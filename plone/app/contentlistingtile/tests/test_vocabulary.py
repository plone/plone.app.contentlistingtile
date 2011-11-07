from mocker import Mocker
from plone.app.contentlistingtile import tile
from plone.app.contentlistingtile.interfaces import IContentListingTileSettings
from plone.mocktestcase import MockTestCase
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.component import provideUtility
from zope.schema.interfaces import IVocabularyTokenized
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import VocabularyRegistryError
from zope.schema.vocabulary import getVocabularyRegistry


class TestAvailableListingViewsVocabulary(MockTestCase):

    def setUp(self):
        super(TestAvailableListingViewsVocabulary, self).setUp()
        self.testcase_mocker = Mocker()

        provideUtility(tile.availableListingViewsVocabulary,
                       name= u"Available Listing Views")

        # mock the registry, so that we have a static
        # configuration in our tests. we test functionality,
        # not configuration..
        proxy = self.testcase_mocker.mock()
        proxy.listing_views
        self.testcase_mocker.result({
                'listing': 'List contents',
                'summary': 'Summarize contents'})
        self.testcase_mocker.count(0, None)

        registry = self.testcase_mocker.mock()
        provideUtility(provides=IRegistry, component=registry)
        registry.forInterface(IContentListingTileSettings)
        self.testcase_mocker.result(proxy)
        self.testcase_mocker.count(0, None)

        # we need to register the vocabulary utility in the
        # vocabulary registry manually at this point:
        vocabulary_registry = getVocabularyRegistry()
        try:
            vocabulary_registry.get(None, u"Available Listing Views")
        except VocabularyRegistryError:
            factory = getUtility(IVocabularyFactory,
                                 name=u"Available Listing Views")
            vocabulary_registry.register(u"Available Listing Views", factory)

        self.testcase_mocker.replay()

    def tearDown(self):
        self.testcase_mocker.verify()
        self.testcase_mocker.restore()
        super(TestAvailableListingViewsVocabulary, self).tearDown()

    def test_returns_vocabulary_with_terms(self):
        vocabulary_registry = getVocabularyRegistry()
        vocabulary = vocabulary_registry.get(None, u"Available Listing Views")

        self.assertTrue(IVocabularyTokenized.providedBy(vocabulary))
        self.assertEqual(len(vocabulary), 2)

    def test_keys_and_labels(self):
        vocabulary_registry = getVocabularyRegistry()
        vocabulary = vocabulary_registry.get(None, u"Available Listing Views")

        terms = list(vocabulary)

        self.assertEqual(terms[0].token, 'listing')
        self.assertEqual(terms[0].value, 'listing')
        self.assertEqual(terms[0].title, 'List contents')

        self.assertEqual(terms[1].token, 'summary')
        self.assertEqual(terms[1].value, 'summary')
        self.assertEqual(terms[1].title, 'Summarize contents')
