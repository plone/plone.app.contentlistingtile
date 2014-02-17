import urllib
from plone.tiles.absoluteurl import BaseTileAbsoluteURL
from plone.tiles.data import TransientTileDataManager, decode
from plone.app.contentlistingtile import PloneMessageFactory as _
from plone.app.contentlistingtile.interfaces import IContentListingTileSettings
from plone.directives import form as directivesform
from plone.formwidget.querystring.widget import QueryStringFieldWidget
from plone.registry.interfaces import IRegistry
from plone.tiles import PersistentTile
from plone.tiles import Tile
from zope import schema
from zope.component import getMultiAdapter, adapts
from zope.component import getUtility
from zope.interface import directlyProvides, implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from plone.tiles.interfaces import ITileDataManager, ITile


class IContentListingTile(directivesform.Schema):
    """A tile that displays a listing of content items"""

    view_template = schema.Choice(title=_(u"Display mode"),
                                  source=_(u"Available Listing Views"),
                                  required=True)

    directivesform.widget(query=QueryStringFieldWidget)
    query = schema.List(title=_(u'Search terms'),
                        value_type=schema.Dict(value_type=schema.Field(),
                                               key_type=schema.TextLine()),
                        description=_(u'Define the search terms for the items '
                                      u'you want to list by choosing what to '
                                      u'match on. The list of results will '
                                      u'be dynamically updated'),
                        required=False,
                        default=[{'i':'path',
                                  'o':'plone.app.querystring.operation.string.relativePath',
                                  'v':'.'}])



class ContentListingTile(Tile):
    """A tile that displays a listing of content items"""

    def __call__(self):
        self.update()
        return self.contents()

    def update(self):
        self.query = self.data.get('query')
        self.view_template = self.data.get('view_template')

    def contents(self):
        """Search results"""

        accessor = getMultiAdapter((self.context, self.request),
                                   name='querybuilderresults')(query=self.query)

        view = self.view_template
        view = view.encode('utf-8')
        options = dict(original_context=self.context)
        return getMultiAdapter((accessor, self.request), name=view)(**options)

class ListingTileAbsoluteURL(BaseTileAbsoluteURL):
    """Override to simplify urls
    """

    def __str__(self):
        url = super(ListingTileAbsoluteURL, self).__str__()
        #we don't need the id
        url = '/'.join(url.split('/')[:-1])

        data = ITileDataManager(self.context).get()
        if data:
            url += '?' + query_encode(data)
        return url


class ListingTileDataManager(TransientTileDataManager):
    """Override to decode simpler urls
    """
    implements(ITileDataManager)
    adapts(ContentListingTile)

    def get(self):
        # If we don't have a schema, just take the request
        if self.tileType is None or self.tileType.schema is None:
            return self.data.copy()

        self.data = query_decode(self.data)
        # Try to decode the form data properly if we can
        try:
            return decode(self.data, self.tileType.schema, missing=True)
        except (ValueError, UnicodeDecodeError,):
            #LOGGER.exception(u"Could not convert form data to schema")
            return self.data.copy()


# turn query into simple data structure

def query_encode(data):
    query = data['query']
    new_data = dict(view_template=data['view_template'])
    for criteria in query:
        i = criteria['i']
        o = criteria['o']
        v = criteria['v']
        #TODO: should use default
        if o != 'plone.app.querystring.operation.selection.is':
            value = "%s|%s" % (o,v)
        else:
            value = v
        new_data[i] = value
    return urllib.urlencode(new_data)

def query_decode(data):
    query = []
    for i,v in data.items():
        if i == data['view_template']:
            continue
        if '|' in v:
            o, v = v.split('|')
        else:
            o = 'plone.app.querystring.operation.selection.is'
        criteria = dict(i=i,o=o,v=v)
        query.append(criteria)
    data['query'] = query
    return data



def availableListingViewsVocabulary(context):
    """Get available views for listing content as vocabulary"""

    registry = getUtility(IRegistry)
    proxy = registry.forInterface(IContentListingTileSettings)
    sorted = proxy.listing_views.items()
    sorted.sort(lambda a, b: cmp(a[1], b[1]))
    voc = []

    for key, label in sorted:
        voc.append(SimpleVocabulary.createTerm(key, key, label))
    return SimpleVocabulary(voc)


directlyProvides(availableListingViewsVocabulary, IVocabularyFactory)
