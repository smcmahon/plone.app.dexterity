import urllib

from OFS.SimpleItem import SimpleItem
from ZPublisher.BaseRequest import DefaultPublishTraverse

from zope.interface import implements, Interface
from zope.cachedescriptors.property import Lazy as lazy_property
from zope.component import adapts, getAllUtilitiesRegisteredFor, getUtility, ComponentLookupError, getSiteManager, getGlobalSiteManager
from zope.publisher.interfaces.browser import IBrowserPublisher
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from zope import schema
from zope.publisher.interfaces.browser import IBrowserRequest

from z3c.form import field, button
from plone.z3cform import layout
from plone.z3cform.crud import crud

from Products.CMFCore.utils import getToolByName

from plone.dexterity.interfaces import IDexterityFTI, IDexterityContent
from plone.dexterity.utils import getAdditionalSchemata
from plone.app.dexterity.interfaces import ITypesContext, ITypeSchemaContext, ITypeSettings
from plone.app.dexterity.interfaces import ITypeStats
from plone.app.dexterity.browser.utils import UTF8Property
from plone.schemaeditor.browser.schema.traversal import SchemaContext
from plone.app.dexterity.browser.layout import TypeFormLayout

from plone.app.dexterity import MessageFactory as _


class IViewRegistration(Interface):

    name = schema.TextLine(title=u'Name')


class TypeViewsListing(crud.CrudForm):
    """ A table of available views for a content type.
    """

    description = _(u'The following views are available for this content type.')
    view_schema = IViewRegistration
    addform_factory = crud.NullForm

    def get_items(self):
        type_schema = self.context.fti.lookupSchema()
        views = dict([(str(reg.name), reg)for reg in getGlobalSiteManager().registeredAdapters()
            if len(reg.required) == 2
            and reg.required[0] is not None
            and reg.required[0] in (type_schema, IDexterityContent)
            and reg.required[1] is not None
            and reg.required[1].isOrExtends(IBrowserRequest)])
        for reg in getSiteManager().registeredAdapters():
            if (len(reg.required) == 2
                and reg.required[0] is not None
                and reg.required[0] in (type_schema, IDexterityContent)
                and reg.required[1] is not None
                and reg.required[1].isOrExtends(IBrowserRequest)):
                views[reg.name] = reg
        return sorted((str(k), v) for k, v in views.items())

    # def remove(self, (id, item)):
    #     """ Remove a content type.
    #     """
    #     ttool = getToolByName(self.context, 'portal_types')
    #     ttool.manage_delObjects([id])

    def link(self, item, field):
        """ Generate links to the edit page for each type.
            (But only for types with schemata that can be edited through the web.)
        """
        try:
            return '%s/edit-view?template_id=%s&view_name=%s' % (self.context.absolute_url(), item.factory.getId(), item.name)
        except:
            pass


class TypeViewsPage(TypeFormLayout):
    form = TypeViewsListing
    label = _(u'Views')
