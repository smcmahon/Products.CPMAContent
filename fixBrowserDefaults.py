# Example code:

# Import a standard function, and get the HTML request and response objects.
from Products.PythonScripts.standard import html_quote
request = container.REQUEST
response =  request.response

# Return a string identifying this script.
print "This is the", script.meta_type, '"%s"' % script.getId(),
if script.title:
    print "(%s)" % html_quote(script.title),
print "in", container.absolute_url()

for brain in context.portal_catalog(portal_type=('StandardFolder', 'Folder')):
    obj = brain.getObject()
    if 'indexhtml' in obj.objectIds():
        obj.setDefaultPage('indexhtml')
        obj.reindexObject()
        print obj

return printed
