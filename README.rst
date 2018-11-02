====================
django-related-admin
====================
.. image:: https://travis-ci.org/PetrDlouhy/django-related-admin.svg?branch=master
    :target: https://travis-ci.org/PetrDlouhy/django-related-admin
.. image:: https://coveralls.io/repos/github/PetrDlouhy/django-related-admin/badge.svg?branch=master
	 :target: https://coveralls.io/github/PetrDlouhy/django-related-admin?branch=master
.. image:: https://badge.fury.io/py/django-related-admin.svg
    :target: https://badge.fury.io/py/django-related-admin

Allow foreign key attributes in Django admin change list ``list_display`` with '__'

This is based on `DjangoSnippet 2996 <https://djangosnippets.org/snippets/2996/>`_ which was made by Kpacn.

Installation
------------

1. This library is on PyPI so you can install it with::

    pip install django-related-admin

or from github::

    pip install git+https://github.com/PetrDlouhy/django-related-admin#egg=django-related-admin

2. Add "related_admin" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'related_admin',
        'django.contrib.admin',
    )

Note: Django-related-admin changes ``change_list.html`` template to disable ``white-space: nowrap;``
css class on admin headers to allow long (posibly related) header names to wrap.
If you want this behaviour, add the app before ``django.contrib.admin``, otherwise after.


Usage
-----

Just use it instead of model.Admin::

   from related_admin import RelatedFieldAdmin
   from related_admin import getter_for_related_field

   class FooAdmin(RelatedFieldAdmin):
       # these fields will work automatically (and boolean fields will display an icon):
       list_display = ('address__phone','address__country__country_code','address__foo')

       # ... but you can also define them manually if you need to override short_description or boolean parameter:
       address__foo = getter_for_related_field('address__foo', short_description='Custom Name', boolean=True)

