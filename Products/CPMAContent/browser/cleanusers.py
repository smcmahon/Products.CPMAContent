from AccessControl import getSecurityManager
from AccessControl import Unauthorized
from Acquisition import aq_get

from zope.interface import implements, Interface
from zope.component import getMultiAdapter

from Products.Five import BrowserView
from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName

from Shared.DC.ZRDB.Results import Results


class ICleanUserView(Interface):
    """
    CleanUser view interface
    """

    pass



class CleanUserView(BrowserView):
    """
    CleanUser browser view
    """
    implements(ICleanUserView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        self.request.response.setHeader('Content-Type', 'text/plain')

        grouptool = getToolByName(self.context, 'portal_groups')
        membertool = getToolByName(self.context, 'portal_membership')
        pas = getToolByName(self.context, 'acl_users')

        user_ids = membertool.listMemberIds()
        group_ids = grouptool.listGroupIds()
        principal_ids = set(user_ids).union(set(group_ids))
        to_remove = [user_id for user_id in pas.mutable_properties._storage.keys()
                     if user_id not in principal_ids]
        res = "About to remove %d users from mutable_properties that have  no corresponding user or group.\n" % len(to_remove)
        for s in to_remove:
            res += "%s\n" % s

        for user_id in to_remove:
            pas.mutable_properties.deleteUser(user_id)
        res += "Removed user ids from mutable_properties: %r" % to_remove

        return res

