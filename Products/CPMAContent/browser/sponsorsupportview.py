from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

# from Products.CPMAContent import CPMAContentMessageFactory as _


class ISponsorSupportView(Interface):
    """
    SponsorSupport view interface
    """

    def test():
        """ test method"""

    def findSponsor(propname):
        """
        propname should be 'MajorSponsor' 'MinorSponsor' or 'MinorSponsor2'
        Looks in sponsors folder for matching PageSponsor (type not checked)
        Checks pub status and returns page sponsor content object.
        """


class SponsorSupportView(BrowserView):
    """
    SponsorSupport browser view
    """
    implements(ISponsorSupportView)

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.portal = getToolByName(self.context, 'portal_url').getPortalObject()
        self.workflow_tool = self.portal.portal_workflow

    # @property
    # def portal_catalog(self):
    #     return getToolByName(self.context, 'portal_catalog')

    def findSponsorId(self, propname):
        # propname should be 'MajorSponsor' 'MinorSponsor' or 'MinorSponsor2'
        # Looks in sponsors folder for matching PageSponsor (type not checked)
        # Returns id

        propval = getattr(self.context, propname, None)
        if not propval:
            return ''

        if propval == 'section_sponsor':
            co = self.context
            while 1:
                co = co.aq_parent
                if co.meta_type not in ['standarddoc', 'standardfolder', 'standardnewsitem', 'standardevent', 'Dexterity Container']:
                    return 'no_sponsor'
                appv = getattr(co, propname, None)
                if appv and appv != 'section_sponsor':
                    return appv
        else:
            return propval

    def findSponsor(self, propname):
        # propname should be 'MajorSponsor' 'MinorSponsor', 'MinorSponsor2' or 'footer-sponsor'
        # Looks in sponsors folder for matching PageSponsor (type not checked)
        # Checks pub status and returns page sponsor content object.

        sponsorId = self.findSponsorId(propname)
        if sponsorId and sponsorId != 'no_sponsor':
            if propname == 'footer_sponsor':
                sponsorFolder = getattr(self.portal, 'footer-sponsors')
            else:
                sponsorFolder = getattr(self.portal, 'sponsors')
            if sponsorFolder:
                sponsor = getattr(sponsorFolder, sponsorId)
                if not self.workflow_tool.getInfoFor(sponsor, 'review_state', '') in ['published', 'visible']:
                    return None
                now = self.context.ZopeTime()
                start_pub = getattr(sponsor, 'effective_date', None)
                end_pub = getattr(sponsor, 'expiration_date', None)

                if start_pub and start_pub > now:
                    return None
                if end_pub and now > end_pub:
                    return None

                return sponsor
        return None

    def test(self):
        """
        test method
        """

        return {
            'MajorSponsor': self.findSponsor('major_sponsor'),
            'MinorSponsor': self.findSponsor('minor_sponsor'),
            'MinorSponsor2': self.findSponsor('minor_sponsor2'),
        }
