## Script (Python) "mapURL"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=address, city, zip, state='CA',
##title=
##
from Products.PythonScripts.standard import html_quote, url_quote_plus

#http://www.mapquest.com/maps/map.adp?&address=274+Cottage+Circle&city=davis&state=ca&zipcode=95616
# return "http://www.mapquest.com/maps/map.adp?&address=%s&city=%s&state=%s&zipcode=%s" % \

return "http://maps.google.com/maps?q=%s,+%s,+%s+%s" % \
 (
   url_quote_plus(address.replace('&', 'and')),
   url_quote_plus("%s" % city),
   url_quote_plus("%s" % state),
   url_quote_plus("%s" % zip),
 )
