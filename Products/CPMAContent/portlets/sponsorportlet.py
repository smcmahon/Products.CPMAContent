from zope.interface import Interface
from zope.interface import implements

from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider

from zope import schema
from zope.component import getMultiAdapter
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.CPMAContent import CPMAContentMessageFactory as _

from zope.i18nmessageid import MessageFactory
__ = MessageFactory("plone")

class ISponsorPortlet(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    # TODO: Add any zope.schema fields here to capture portlet configuration
    # information. Alternatively, if there are no settings, leave this as an
    # empty interface - see also notes around the add form and edit form
    # below.

    # some_field = schema.TextLine(title=_(u"Some field"),
    #                              description=_(u"A field to use"),
    #                              required=True)

    sponsorType =schema.Choice(
                title=_(u"Sponsor Type"),
                values=[_(u'Major'), _(u'Minor'), _(u'Second Minor')]
            )


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(ISponsorPortlet)

    # TODO: Set default values for the configurable parameters here

    # some_field = u""

    # TODO: Add keyword parameters for configurable parameters here
    def __init__(self, sponsorType=u'Major'):
        self.sponsorType = sponsorType

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return __(u"Sponsor Portlet")


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('sponsorportlet.pt')

    def test(self):
        """ test code """

        return self.data.sponsorType

    def getSponsor(self):
        """ return the page/section sponsor """

        stype = self.data.sponsorType
        if stype == 'Major':
            sponsorType = 'major_sponsor'
        elif stype == 'Minor':
            sponsorType = 'minor_sponsor'
        elif stype == 'Second Minor':
            sponsorType = 'minor_sponsor2'
        else:
            return None

        sponsorSupport = getMultiAdapter((self.context.aq_inner, self.request), name="sponsorsupport_view")
        return sponsorSupport.findSponsor(sponsorType)


# NOTE: If this portlet does not have any configurable parameters, you can
# inherit from NullAddForm and remove the form_fields variable.

class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(ISponsorPortlet)

    def create(self, data):
        return Assignment(**data)


# NOTE: IF this portlet does not have any configurable parameters, you can
# remove this class definition and delete the editview attribute from the
# <plone:portlet /> registration in configure.zcml

class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(ISponsorPortlet)
