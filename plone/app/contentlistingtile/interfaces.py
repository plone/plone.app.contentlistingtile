from plone.app.contentlistingtile import PloneMessageFactory as _
from zope import schema
from zope.interface import Interface


class IContentListingTileSettings(Interface):
    """Settings for the content listing tile."""

    listing_views = schema.Dict(title=_(u"Listing views"),
                                description=_(u"Listing views available for "
                                              "the content listing tile"),
                                key_type=schema.TextLine(),
                                value_type=schema.TextLine())
