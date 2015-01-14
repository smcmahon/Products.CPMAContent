## Controller Python Script "editMember_action"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=id=None
##title=
##
# handle member profile edit

view = context.restrictedTraverse('@@findpod_view')

form = context.REQUEST.form
schooling = form.get('schooling', '').strip()
residency = form.get('residency', '').strip()
specialties = form.get('specialties', '').strip()
insurance = form.get('insurance', '').strip()
hours = form.get('hours', '').strip()
affiliations = form.get('affiliations', '').strip()
address2 = form.get('address2', '').strip()
city2 = form.get('city2', '').strip()
state2 = form.get('state2', '').strip()
zip2 = form.get('zip2', '').strip()
phone2 = form.get('phone2', '').strip()
hours2 = form.get('hours2', '').strip()
address3 = form.get('address3', '').strip()
city3 = form.get('city3', '').strip()
state3 = form.get('state3', '').strip()
zip3 = form.get('zip3', '').strip()
phone3 = form.get('phone3', '').strip()
hours3 = form.get('hours3', '').strip()
website = form.get('website', '').strip()
certifications = form.get('certifications', '').strip()
hospitals = form.get('hospitals', '').strip()
id = int(form.get('member_id', '').strip())
rec = int(form.get('rec').strip())

if website and (website.lower().find('http') != 0):
    website = "http://%s" % website

if not zip2:
    zip2 = 0
if not zip3:
    zip3 = 0

view.insertMemberProfile(id=id,
   schooling=schooling,
   specialties=specialties,
   residency=residency,
   insurance=insurance,
   hours=hours,
   affiliations=affiliations,
   address2=address2,
   city2=city2,
   state2=state2,
   zip2=zip2,
   phone2=phone2,
   hours2=hours2,
   address3=address3,
   city3=city3,
   state3=state3,
   zip3=zip3,
   phone3=phone3,
   hours3=hours3,
   website=website,
   certifications=certifications,
   hospitals=hospitals
   )

     
if not view.canEditHere():
    message = """
URL: %s/showMember?rec=%s
Member Name: %s
Member ID: %s

Secondary practice #1:
%s
%s
%s, %s %s

Secondary practice #2:
%s
%s
%s, %s %s

Primary Hours:
%s

Secondary Hours:
%s

Specialities:
%s

Board Certifications:
%s

Hospital Affiliations:
%s

Insurance:
%s

Schooling:
%s

Residency:
%s

Professional Affiliations:
%s

Website:
%s
""" % (container.absolute_url(), rec, form.get('member_name', ''), id, phone2, address2, city2, state2, zip2, hours2, phone3, address3, city3, state3, zip3, hours3, hours, specialties, certifications, hospitals, insurance, schooling, residency, affiliations, website)
    context.MailHost.simple_send('steve@dcn.org', 'postmaster@reidmcmahon.com', "Update of Member Profile via Website", message)
    # context.MailHost.simple_send('afinley@podiatrists.org', 'postmaster@reidmcmahon.com', "Update of Member Profile via Website", message)


state.setKwargs( {'portal_status_message':'Record updated.', 'rec':rec} )

# state.setNextAction('redirect_to:string:${portal_url}/visitors/findpod/showMember')
state.setNextAction('redirect_to:string:showMember')

# Always make sure to return the ControllerState object
return state
