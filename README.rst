====================
django-related-admin
====================

Allow foreign key attributes in list_display with '__'

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
    )

Usage
-----

Just use it instead of model.Admin::

   from related_admin import RelatedFieldAdmin

   class FooAdmin(RelatedFieldAdmin):
       # these fields will work automatically:
       list_display = ('address__phone','address__country__country_code','address__foo')

       # ... but you can also define them manually if you need to override short_description:
       address__foo = getter_for_related_field('address__foo', short_description='Custom Name')

