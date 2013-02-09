from z3c.form import button
from z3c.form import form

from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile

from plone.z3cform.layout import wrap_form

from Products.CMFCore.utils import getToolByName

from plone.dexterity.fti import DexterityFTI

from plone.app.dexterity import MessageFactory as _

from plone.app.dexterity.interfaces import ITypesContext

from plone.supermodel import serializeModel


class FullEggExportForm(form.Form):

    label = _(u'Full egg export')
    id = 'full-egg-export-form'
    template = ViewPageTemplateFile('egg_export.pt')

    def get_schema_models(self):
        pt = getToolByName(self.context, 'portal_types')
        items = self.request.get('selected')

        results = []

        if items:
            items = items.split(',')

            for item in items:
                text = serializeModel(pt[item].lookupModel())

                results.append({'ct_name': item,
                                'xml_model': text})

        return results

    @button.buttonAndHandler(_('Lay an egg'), name='export-egg')
    def exportEgg(self, action):
        items = self.request.form.get('form.selected')
        if items:
            items = items.split(',')
            for item in items:
                pass

    def nextURL(self):
        return self.context.aq_parent.absolute_url()

FullEggExportFormPage = wrap_form(FullEggExportForm)
