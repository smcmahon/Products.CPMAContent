import random
import re

from Acquisition import aq_get
import transaction

from zope.interface import implements, Interface
from zope.component import getMultiAdapter

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from Shared.DC.ZRDB.Results import Results


class IUpdatePodView(Interface):
    """
    Update Podiatrists from db view interface
    """

    def processForm():
        """ process the form, return messages """


class UpdatePodView(BrowserView):
    """
    FindPod browser view
    """
    implements(IUpdatePodView)

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.dbc = aq_get(context, 'cpma_writer')
        self.writer = self.dbc()
        self.messages = []
        self.zipsupport = getMultiAdapter((self.context, self.request), name=u"zipsupport_view")
        self.regtool = getToolByName(context, 'portal_registration')

    def find_lat_lon(self, zip):
        zres = self.zipsupport.queryByZip(zip)
        if len(zres):
            return zres[0].lat, zres[0].lon
        else:
            return 0.0, 0.0

    def createUser(self, username, fullname, email, passwd=None):
        if passwd is None:
            passwd = str(random.randint(1, 1000000000L))

        username = str(username.lower())

        # This is minimum required information set
        # to create a working member
        properties = {
            'username': username,
            # Full name must be always as utf-8 encoded
            'fullname': fullname.encode("utf-8"),
            'email': email,
        }

        try:
            # addMember() returns MemberData object
            self.regtool.addMember(username, passwd, properties=properties)
            transaction.get().commit()
        except ValueError:
            # Give user visual feedback what went wrong
            self.messages.append("Could not create the user: %s" % username)
            return None

    def processRecords(self, upload):
        newUsers = 0
        oldUsers = 0
        existingUsers = self.context.acl_users.getUserNames()

        count = -1
        for line in upload.xreadlines():
            count += 1
            if count == 0:
                if line.find("Member_Type\tID\tFIRST_NAME\tLAST_NAME\tDESIGNATION\tCompany\tADDRESS_1\tADDRESS_2\tCITY\tSTATE_PROVINCE\tZIP\tWORK_PHONE\tFAX\tEMAIL") == 0:
                    is_member = 'Y'
                    self.messages.append('Member Database')
                # elif line.find("FULL_NAME\tID") == 0:
                #     is_member = 'N'
                #     self.messages.append('Non-Member Database')
                else:
                    self.messages.append("Input file not formatted as expected!")
                    self.messages.append("No changes made.")
                    return
                self.messages.append('Member database cleared in preparation for update.')
                self.writer.query('delete from members')
                self.writer.query('delete from locations where secondary="N"')
                continue

            #compact spaces
            line = re.sub(' +', ' ', line.replace('"', '').strip())
            if not line:
                count -= 1
                continue
            #clean and split
            aline = [s.strip() for s in line.split('\t')]
            if is_member == 'Y':
                while len(aline) < 14:
                    aline.append('')
                MTYPE, ID, FIRST_NAME, LAST_NAME, DESIGNATION, COMPANY, \
                ADDRESS_1, ADDRESS_2, CITY, STATE_PROVINCE, ZIP, WORK_PHONE, \
                FAX, EMAIL = aline
            # else:
            #     while len(aline) < 20:
            #         aline.append('')
            #     FULL_NAME, ID, APMA_NO, MAJOR_KEY, FIRST_NAME, MIDDLE_NAME, \
            #     LAST_NAME, DESIGNATION, WORK_PHONE, FAX, TOLL_FREE, ADDRESS_1, \
            #     ADDRESS_2, CITY, STATE_PROVINCE, ZIP, EMAIL, LAST_FIRST, Title, Company = aline

            if is_member == 'Y':
                if MTYPE in ('5.4', 'A1', 'A1X', 'A2', 'A2X', 'A3', 'A3X', 'A4', 'A4X', 'AC', 'FA', 'SE',):
                    public = 'Y'
                else:
                    public = 'N'

                address = ADDRESS_1
                if ADDRESS_2:
                    address = "%s\n%s" % (address, ADDRESS_2)

                try:
                    zip5 = int(ZIP[:5])
                except:
                    zip5 = 0
                lat, lon = self.find_lat_lon(zip5)

                icmd = """insert into members values (0, %s,"%s","%s","%s","%s","%s","%s","%s", %d, %g, %g, "%s", "%s", "%s", "%s")""" % \
                 (ID, FIRST_NAME, LAST_NAME, DESIGNATION, WORK_PHONE, address, \
                 CITY, STATE_PROVINCE, zip5, lat, lon, public, COMPANY, FAX, EMAIL)
                self.writer.query(icmd)
                # cpma_cursor.execute(icmd)

                if zip5 != 0:
                    icmd = """insert into locations values (%s,"%s","%s", %d, %g, %g, "N")""" % \
                     (ID, CITY, STATE_PROVINCE, zip5, lat, lon)
                    self.writer.query(icmd)
                    # cpma_cursor.execute(icmd)

                if ID not in existingUsers:
                    fullname = "%s %s" % (FIRST_NAME, LAST_NAME)
                    if FIRST_NAME:
                        pwd = "%s%s" % (FIRST_NAME[0], LAST_NAME)
                    else:
                        pwd = LAST_NAME
                    self.createUser(ID, fullname, 'noreply@podiatrists.org', passwd=pwd.lower())
                    newUsers += 1
                else:
                    oldUsers += 1

        self.messages.append("%d records processed." % count)
        self.messages.append("%d members added." % newUsers)
        self.messages.append("%d members updated." % oldUsers)

        if is_member == 'Y':
            # prune locations
            icmd = """SELECT DISTINCT locations.id FROM locations left join members on members.id = locations.id where members.id is null"""
            to_delete = Results(self.writer.query(icmd))
            for user in [r.id for r in to_delete]:
                icmd = """DELETE FROM locations WHERE id="%s" """ % user
                self.writer.query(icmd)
            if len(to_delete):
                self.messages.append("Deleted secondary location(s) for %d users no longer in database." % len(to_delete))

    def processForm(self):
        """ process the form, return messages """

        form = self.request.form
        upload = form.get('uploadfile')
        if upload:
            self.processRecords(upload)
        return '\n\n'.join(self.messages)
