Introduction
============

This is a full-blown functional test. The emphasis here is on testing what
the user may input and see, and the system is largely tested as a black box.
We use PloneTestCase to set up this test as well, so we have a full Plone site
to play with. We *can* inspect the state of the portal, e.g. using 
self.portal and self.folder, but it is often frowned upon since you are not
treating the system as a black box. Also, if you, for example, log in or set
roles using calls like self.setRoles(), these are not reflected in the test
browser, which runs as a separate session.

Being a doctest, we can tell a story here.

First, we must perform some setup. We use the testbrowser that is shipped
with Five, as this provides proper Zope 2 integration. Most of the 
documentation, though, is in the underlying zope.testbrower package.

    >>> from Products.Five.testbrowser import Browser
    >>> browser = Browser()
    >>> portal_url = self.portal.absolute_url()

The following is useful when writing and debugging testbrowser tests. It lets
us see all error messages in the error_log.

    >>> self.portal.error_log._ignored_exceptions = ()

With that in place, we can go to the portal front page and log in. We will
do this using the default user from PloneTestCase:

    >>> from Products.PloneTestCase.setup import portal_owner, default_password

Because add-on themes or products may remove or hide the login portlet, this test will use the login form that comes with plone.  

    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()

Here, we set the value of the fields on the login form and then simulate a
submit click.  We then ensure that we get the friendly logged-in message:

    >>> "You are now logged in" in browser.contents
    True

Finally, let's return to the front page of our site before continuing

    >>> browser.open(portal_url)

-*- extra stuff goes here -*-
The StandardEvent content type
===============================

In this section we are tesing the StandardEvent content type by performing
basic operations like adding, updadating and deleting StandardEvent content
items.

Adding a new StandardEvent content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'StandardEvent' and click the 'Add' button to get to the add form.

    >>> browser.getControl('StandardEvent').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'StandardEvent' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'StandardEvent Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'StandardEvent' content item to the portal.

Updating an existing StandardEvent content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New StandardEvent Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New StandardEvent Sample' in browser.contents
    True

Removing a/an StandardEvent content item
--------------------------------

If we go to the home page, we can see a tab with the 'New StandardEvent
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New StandardEvent Sample' in browser.contents
    True

Now we are going to delete the 'New StandardEvent Sample' object. First we
go to the contents tab and select the 'New StandardEvent Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New StandardEvent Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New StandardEvent
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New StandardEvent Sample' in browser.contents
    False

Adding a new StandardEvent content item as contributor
------------------------------------------------

Not only site managers are allowed to add StandardEvent content items, but
also site contributors.

Let's logout and then login as 'contributor', a portal member that has the
contributor role assigned.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = 'contributor'
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

We select 'StandardEvent' and click the 'Add' button to get to the add form.

    >>> browser.getControl('StandardEvent').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'StandardEvent' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'StandardEvent Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new StandardEvent content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)


The PageSponsor content type
===============================

In this section we are tesing the PageSponsor content type by performing
basic operations like adding, updadating and deleting PageSponsor content
items.

Adding a new PageSponsor content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'PageSponsor' and click the 'Add' button to get to the add form.

    >>> browser.getControl('PageSponsor').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'PageSponsor' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'PageSponsor Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'PageSponsor' content item to the portal.

Updating an existing PageSponsor content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New PageSponsor Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New PageSponsor Sample' in browser.contents
    True

Removing a/an PageSponsor content item
--------------------------------

If we go to the home page, we can see a tab with the 'New PageSponsor
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New PageSponsor Sample' in browser.contents
    True

Now we are going to delete the 'New PageSponsor Sample' object. First we
go to the contents tab and select the 'New PageSponsor Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New PageSponsor Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New PageSponsor
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New PageSponsor Sample' in browser.contents
    False

Adding a new PageSponsor content item as contributor
------------------------------------------------

Not only site managers are allowed to add PageSponsor content items, but
also site contributors.

Let's logout and then login as 'contributor', a portal member that has the
contributor role assigned.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = 'contributor'
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

We select 'PageSponsor' and click the 'Add' button to get to the add form.

    >>> browser.getControl('PageSponsor').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'PageSponsor' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'PageSponsor Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new PageSponsor content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)


The SponsorFolder content type
===============================

In this section we are tesing the SponsorFolder content type by performing
basic operations like adding, updadating and deleting SponsorFolder content
items.

Adding a new SponsorFolder content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'SponsorFolder' and click the 'Add' button to get to the add form.

    >>> browser.getControl('SponsorFolder').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'SponsorFolder' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'SponsorFolder Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'SponsorFolder' content item to the portal.

Updating an existing SponsorFolder content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New SponsorFolder Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New SponsorFolder Sample' in browser.contents
    True

Removing a/an SponsorFolder content item
--------------------------------

If we go to the home page, we can see a tab with the 'New SponsorFolder
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New SponsorFolder Sample' in browser.contents
    True

Now we are going to delete the 'New SponsorFolder Sample' object. First we
go to the contents tab and select the 'New SponsorFolder Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New SponsorFolder Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New SponsorFolder
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New SponsorFolder Sample' in browser.contents
    False

Adding a new SponsorFolder content item as contributor
------------------------------------------------

Not only site managers are allowed to add SponsorFolder content items, but
also site contributors.

Let's logout and then login as 'contributor', a portal member that has the
contributor role assigned.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = 'contributor'
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

We select 'SponsorFolder' and click the 'Add' button to get to the add form.

    >>> browser.getControl('SponsorFolder').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'SponsorFolder' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'SponsorFolder Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new SponsorFolder content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)


The StandardDoc content type
===============================

In this section we are tesing the StandardDoc content type by performing
basic operations like adding, updadating and deleting StandardDoc content
items.

Adding a new StandardDoc content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'StandardDoc' and click the 'Add' button to get to the add form.

    >>> browser.getControl('StandardDoc').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'StandardDoc' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'StandardDoc Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'StandardDoc' content item to the portal.

Updating an existing StandardDoc content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New StandardDoc Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New StandardDoc Sample' in browser.contents
    True

Removing a/an StandardDoc content item
--------------------------------

If we go to the home page, we can see a tab with the 'New StandardDoc
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New StandardDoc Sample' in browser.contents
    True

Now we are going to delete the 'New StandardDoc Sample' object. First we
go to the contents tab and select the 'New StandardDoc Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New StandardDoc Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New StandardDoc
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New StandardDoc Sample' in browser.contents
    False

Adding a new StandardDoc content item as contributor
------------------------------------------------

Not only site managers are allowed to add StandardDoc content items, but
also site contributors.

Let's logout and then login as 'contributor', a portal member that has the
contributor role assigned.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = 'contributor'
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

We select 'StandardDoc' and click the 'Add' button to get to the add form.

    >>> browser.getControl('StandardDoc').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'StandardDoc' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'StandardDoc Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new StandardDoc content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)


The StandardFolder content type
===============================

In this section we are tesing the StandardFolder content type by performing
basic operations like adding, updadating and deleting StandardFolder content
items.

Adding a new StandardFolder content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'StandardFolder' and click the 'Add' button to get to the add form.

    >>> browser.getControl('StandardFolder').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'StandardFolder' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'StandardFolder Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'StandardFolder' content item to the portal.

Updating an existing StandardFolder content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New StandardFolder Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New StandardFolder Sample' in browser.contents
    True

Removing a/an StandardFolder content item
--------------------------------

If we go to the home page, we can see a tab with the 'New StandardFolder
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New StandardFolder Sample' in browser.contents
    True

Now we are going to delete the 'New StandardFolder Sample' object. First we
go to the contents tab and select the 'New StandardFolder Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New StandardFolder Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New StandardFolder
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New StandardFolder Sample' in browser.contents
    False

Adding a new StandardFolder content item as contributor
------------------------------------------------

Not only site managers are allowed to add StandardFolder content items, but
also site contributors.

Let's logout and then login as 'contributor', a portal member that has the
contributor role assigned.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = 'contributor'
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

We select 'StandardFolder' and click the 'Add' button to get to the add form.

    >>> browser.getControl('StandardFolder').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'StandardFolder' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'StandardFolder Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new StandardFolder content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)



