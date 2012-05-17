from zope.component import createObject, getMultiAdapter
from zope.interface import Interface
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

class ViewEditorView(BrowserView):

	def __call__(self):
		return self.index()

	@property
	def template(self):
		template_id = self.request.get('template_id', None)
		if template_id:
			pvc = getToolByName(self.context, 'portal_view_customizations')
			return getattr(pvc, template_id)

	@property
	def template_source(self):
		return self.template.read()

	@property
	def view_name(self):
		return self.request.get('view_name')


class ViewEditorPreview(BrowserView):

	def __call__(self):
		context = createObject(self.context.fti.factory).__of__(self.context)
		view_name = self.request.form.get('view_name')
		view = getMultiAdapter((context, self.request), Interface, name=view_name).__of__(context)
		return view()
