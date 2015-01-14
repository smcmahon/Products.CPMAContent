from AccessControl import getSecurityManager
from AccessControl import Unauthorized
from Acquisition import aq_get

from zope.interface import implements, Interface
from zope.component import getMultiAdapter

from Products.Five import BrowserView
from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName

from Shared.DC.ZRDB.Results import Results


class IFindPodView(Interface):
    """
    FindPod view interface
    """

    def queryCities():
        """ return available cities """

    def queryByCity(city, publicOnly):
        """ return tuples of fname, lname, designation, locations.city, rec """

    def queryById(id, publicOnly):
        """ return tuples of member records """

    def queryByLatLon(LowLat, HighLat, LowLon, HighLon, publicOnly='N'):
        """ return tuples of fname, lname, designation, locations.city, rec """

    def queryByName(fname, publicOnly):
        """ return tuples of fname, lname, designation, locations.city, rec """

    def queryByRec(rec, publicOnly):
        """ return tuple of dicts """

    def queryRecById(id):
        """ return rec """

    def searchCat(anon=True):
        """
            Supplies SQL query results for Find A Podiatrist
        """

    def canEditHere():
        """ current user has edit permissions here """

    def isCurrentUser(id):
        """ current plone user and id match """

    def insertMemberProfile(id,
            schooling,
            specialties,
            residency,
            insurance,
            affiliations,
            hours,
            address2,
            city2,
            state2,
            zip2,
            phone2,
            hours2,
            address3,
            city3,
            state3,
            zip3,
            phone3,
            hours3,
            website,
            certifications,
            hospitals
            ):
        """ Update member's profile; check auth first """


class FindPodView(BrowserView):
    """
    FindPod browser view
    """
    implements(IFindPodView)

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.dbc = aq_get(context, 'cpma_reader')
        self.reader = self.dbc()
        self.mtool = getToolByName(context, 'portal_membership')
        self.isAnon = self.mtool.isAnonymousUser() or self.context.getId() != 'memberdirectory'

    def queryCities(self):
        """ return available cities """

        query = """
            SELECT DISTINCT city FROM locations
            WHERE state = 'CA'
            ORDER BY city
        """

        return [c[0] for c in self.reader.query(query)[1]]

    def queryByCity(self, cities, publicOnly='N'):
        """ return results: fname, lname, designation, locations.city, rec, company """

        if self.isAnon:
            limit = "AND public='Y'"
        else:
            limit = ''

        if type(cities) == type(''):
            cities = (cities,)

        cities = ', '.join([self.dbc.sql_quote__(city) for city in cities])

        query = """
            SELECT DISTINCT fname, lname, designation, locations.city, rec, company
            FROM members
            LEFT JOIN locations ON members.id = locations.id
            WHERE locations.city IN (%s) %s
            ORDER BY locations.city, lname, fname
        """ % (cities, limit)

        return Results(self.reader.query(query))

    def queryById(self, id):
        """ return tuples of member records """

        if self.isAnon:
            limit = "AND public='Y'"
        else:
            limit = ''

        query = """
            select * from members where id = %d %s
        """ % (id, limit)

        return self.reader.query(query)[1]

    def queryByLatLon(self, LowLat, HighLat, LowLon, HighLon):
        """ return Results: fname, lname, designation, locations.city, rec, company """

        if self.isAnon:
            limit = "AND public='Y'"
        else:
            limit = ''

        query = """
            SELECT DISTINCT fname, lname, designation, locations.city, rec, company
            FROM members
            LEFT JOIN locations ON members.id = locations.id
            WHERE
             (locations.lat BETWEEN %g AND %g) AND
             (locations.lon BETWEEN %g AND %g)
            %s
            ORDER BY locations.city, lname, fname
        """ % (LowLat, HighLat, LowLon, HighLon, limit)

        return Results(self.reader.query(query))

    def queryByName(self, fname):
        """ return Results: fname, lname, designation, locations.city, rec, company """

        if self.isAnon:
            limit = "AND public='Y'"
        else:
            limit = ''

        fname = self.dbc.sql_quote__(fname.replace('%', '')).strip("'")

        query = """
            SELECT DISTINCT fname, lname, designation, locations.city, rec, company
            FROM members
            LEFT JOIN locations ON members.id = locations.id
            WHERE
             (lname LIKE '%s%%' OR fname LIKE '%s%%')
             %s
            ORDER BY lname, fname
        """ % (fname, fname, limit)

        return Results(self.reader.query(query))

    def queryByRec(self, rec):
        """ return Results """

        try:
            rec = int(rec)
        except ValueError:
            rec = 99999

        if self.isAnon:
            limit = "AND public='Y'"
        else:
            limit = ''

        query = """
            SELECT members.*,
             schooling, specialties, insurance, residency, hours,
             address2, city2, state2, zip2, phone2, hours2,
             address3, city3, state3, zip3, phone3, hours3,
             affiliations, website, certifications, hospitals
            FROM members
            LEFT JOIN profiles ON profiles.id = members.id
            WHERE rec=%d %s
        """ % (rec, limit)

        return Results(self.reader.query(query))

    def queryRecById(self, id):
        """ return rec """

        query = """select rec from members where id=%d""" % id
        res = self.reader.query(query)[1]

        if len(res):
            return res[0][0]
        else:
            return None

    def searchCat(self):
        """
            Supplies SQL query results for Find A Podiatrist

            If passed a zip code (as request.zip), use ZipSupport
            to get latitude and longitude brackets, then search
            within those brackets.
            If no zip, pick correct query

            To Do: take zip results as candidates and compute
            something closer to actual mileage.
        """

        request = self.request

        fname = request.get('fname', None)
        if fname:
            return self.queryByName(fname=fname)

        city = request.get('city', None)
        if city:
            return self.queryByCity(cities=city)

        zip = request.get('zip', 0)
        try:
            zip = int(zip)
        except ValueError:
            return []
        if zip:
            zipsupport = getMultiAdapter((self.context, self.request), name=u"zipsupport_view")
            radius = request.get('radius', 20)
            lat, lon, LowLat, HighLat, LowLon, HighLon = \
              zipsupport.findCandidateBracket(zip=zip, radius=int(radius))
            return self.queryByLatLon(LowLat=LowLat, HighLat=HighLat, LowLon=LowLon, HighLon=HighLon)

        return []

    def canEditHere(self):
        """ current user has edit permissions here """

        return getSecurityManager().checkPermission(permissions.ModifyPortalContent, self.context)

    def isCurrentUser(self, id):
        """ current plone user and id match """

        return self.mtool.getAuthenticatedMember().id == str(id)

    def insertMemberProfile(self,
            id,
            schooling,
            specialties,
            residency,
            insurance,
            affiliations,
            hours,
            address2,
            city2,
            state2,
            zip2,
            phone2,
            hours2,
            address3,
            city3,
            state3,
            zip3,
            phone3,
            hours3,
            website,
            certifications,
            hospitals
            ):
        """ insert member's profile; check auth first """

        id = int(id)

        if not (self.canEditHere() or self.isCurrentUser(id)):
            raise Unauthorized

        dbc = aq_get(self.context, 'cpma_writer')
        writer = dbc()

        sql_quote = dbc.sql_quote__

        try:
            zip1 = str(int(zip2))
        except ValueError:
            zip2 = ''
        try:
            zip1 = str(int(zip3))
        except ValueError:
            zip3 = ''

        query = """
            DELETE FROM profiles
            WHERE id = %d
            """ % id
        writer.query(query)

        query = """
            INSERT INTO profiles
            SET
                id = %d,
                schooling = %s,
                specialties = %s,
                residency = %s,
                insurance = %s,
                affiliations = %s,
                hours = %s,
                address2 = %s,
                city2 = %s,
                state2 = %s,
                zip2 = '%s',
                phone2 = %s,
                hours2 = %s,
                address3 = %s,
                city3 = %s,
                state3 = %s,
                zip3 = '%s',
                phone3 = %s,
                hours3 = %s,
                website = %s,
                certifications = %s,
                hospitals = %s
        """ % (
            id,
            sql_quote(schooling.strip()),
            sql_quote(specialties.strip()),
            sql_quote(residency.strip()),
            sql_quote(insurance.strip()),
            sql_quote(affiliations.strip()),
            sql_quote(hours.strip()),
            sql_quote(address2.strip()),
            sql_quote(city2.strip()),
            sql_quote(state2.strip()),
            zip2,
            sql_quote(phone2.strip()),
            sql_quote(hours2.strip()),
            sql_quote(address3.strip()),
            sql_quote(city3.strip()),
            sql_quote(state3.strip()),
            zip3,
            sql_quote(phone3.strip()),
            sql_quote(hours3.strip()),
            sql_quote(website.strip()),
            sql_quote(certifications.strip()),
            sql_quote(hospitals.strip())
            )
        writer.query(query)

        # update secondary locations.
        # first, clear
        query = """
            DELETE FROM locations
            WHERE id = %d AND secondary = 'Y'
         """ % id
        writer.query(query)

        if zip2:
            # find the lat & lon for secondary address
            zipsupport = getMultiAdapter((self.context, self.request), name=u"zipsupport_view")
            zres = zipsupport.queryByZip(zip2)
            if len(zres):
                lat = zres[0].lat
                lon = zres[0].lon

                query = """
                    INSERT INTO locations
                    SET
                        id = %d,
                        city = %s,
                        state = %s,
                        zip = %s,
                        lat = %g,
                        lon = %g,
                        secondary = 'Y'
                """ % (
                    id,
                    sql_quote(city2.strip()),
                    sql_quote(state2.strip()),
                    zip2,
                    lat,
                    lon)
                writer.query(query)

        if zip3:
            # find the lat & lon for secondary address
            zipsupport = getMultiAdapter((self.context, self.request), name=u"zipsupport_view")
            zres = zipsupport.queryByZip(zip3)
            if len(zres):
                lat = zres[0].lat
                lon = zres[0].lon

                query = """
                    INSERT INTO locations
                    SET
                        id = %d,
                        city = %s,
                        state = %s,
                        zip = %s,
                        lat = %g,
                        lon = %g,
                        secondary = 'Y'
                """ % (
                    id,
                    sql_quote(city3.strip()),
                    sql_quote(state3.strip()),
                    zip3,
                    lat,
                    lon)
                writer.query(query)

