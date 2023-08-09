# -*- coding: utf-8 -*-
"""
Admin for related fields based on http://djangosnippets.org/snippets/2887/

for Django 1.5 where __metaclass__ is deprecated

"""

from __future__ import absolute_import

from django.contrib import admin
from django.contrib.admin.utils import display_for_field, lookup_field
from django.core import exceptions
from django.db import models


def is_field_allowed(name, field_filter=None):
    """
        Check is field name is eligible for being split.

        For example, '__str__' is not, but 'related__field' is.
    """
    if field_filter in ["year", "month", "week", "day", "hour", "minute", "second"]:
        return False
    return isinstance(name, str) and not name.startswith('__') and not name.endswith('__') and '__' in name


def getter_for_related_field(name, admin_order_field=None, short_description=None, boolean=None):
    """
        Create a function that can be attached to a ModelAdmin to use as a list_display field, e.g:
        client__name = getter_for_related_field('client__name', short_description='Client')
    """
    related_names = name.split('__')

    def getter(self, obj):
        last_obj = obj
        related_name = None

        for related_name in related_names:
            last_obj = obj
            try:
                obj = getattr(obj, "get_%s_display" % related_name)()
            except AttributeError:
                obj = getattr(obj, related_name, None)
        if callable(obj):
            obj = obj()
        elif isinstance(last_obj, models.Model):
            f, attr, value = lookup_field(related_name, last_obj, self)
            empty_value_display = self.get_empty_value_display()
            empty_value_display = getattr(attr, 'empty_value_display', empty_value_display)
            obj = display_for_field(value, f, empty_value_display)
        return obj
    getter.boolean = boolean
    getter.admin_order_field = admin_order_field or name
    getter.short_description = short_description or ' '.join(r.title().replace('_', ' ') for r in related_names)
    return getter


class RelatedFieldAdminMetaclass(type(admin.ModelAdmin)):
    """
        Metaclass used by RelatedFieldAdmin to handle fetching of related field values.
        We have to do this as a metaclass because Django checks that list_display fields are supported by the class.
    """
    def __new__(cls, name, bases, attrs):
        new_class = super(RelatedFieldAdminMetaclass, cls).__new__(cls, name, bases, attrs)

        for field in new_class.list_display:
            if isinstance(field, str) and '__' in field[1:-1] and not hasattr(new_class, field):
                setattr(new_class, field, getter_for_related_field(field))

        return new_class


class RelatedFieldAdmin(admin.ModelAdmin, metaclass=RelatedFieldAdminMetaclass):
    """
        Version of ModelAdmin that can use related fields in list_display, e.g.:
        list_display = ('address__city', 'address__country__country_code')
    """

    def select_related_fk(self, request, qs, select_related):
        # Include all foreign key fields in queryset.
        # This is based on ChangeList.get_query_set().
        # We have to duplicate it here because select_related() only works once.
        # Can't just use list_select_related because we might have multiple__depth__fields it won't follow.
        model = qs.model
        for field_name in self.get_list_display(request):
            try:
                field = model._meta.get_field(field_name)
            except exceptions.FieldDoesNotExist:
                continue
            remote_field = field.remote_field
            if isinstance(remote_field, models.ManyToOneRel):
                select_related.append(field_name)

    def get_queryset(self, request):
        qs = super(RelatedFieldAdmin, self).get_queryset(request)

        # include all related fields in queryset
        select_related = []
        for field in self.get_list_display(request):
            if isinstance(field, str):
                split = field.rsplit('__', 1)
                base = split[0]
                try:
                    field_filter = split[1]
                except IndexError:
                    field_filter = None
                if is_field_allowed(field, field_filter):
                    select_related.append(base)

        # explicitly add contents of self.list_select_related to select_related
        list_select_related = self.get_list_select_related(request)
        if list_select_related and type(list_select_related) is not bool:
            select_related += list_select_related

        self.select_related_fk(request, qs, select_related)
        qs.select_related(*select_related)
        return qs

##################################################################################################### 20230809

from django.contrib.admin import utils
def label_for_field(name, model, model_admin=None, return_attr=False, form=None):
    """
    Return a sensible label for a field name. The name can be a callable,
    property (but not created with @property decorator), or the name of an
    object's attribute, as well as a model field. If return_attr is True, also
    return the resolved attribute (which could be a callable). This will be
    None if (and only if) the name refers to a field.
    """
    attr = None

    try:
        field = utils._get_non_gfk_field(model._meta, name)
        try:
            label = field.verbose_name
        except AttributeError:
            # field is likely a ForeignObjectRel
            label = field.related_model._meta.verbose_name
    except utils.FieldDoesNotExist:



        if name == "__str__":
            label = str(model._meta.verbose_name)
            attr = str
        elif name.find("__") != -1:     ######################################## here fix
            sp = name.split("__")
            mfield_str = sp[0]
            rfield_str = sp[1]

            field = getattr(model, mfield_str).field
            mmodel = field.related_model

            label = str(mmodel._meta.get_field(rfield_str).verbose_name)
            attr = str

        else:
            if callable(name):
                attr = name
            elif hasattr(model_admin, name):
                attr = getattr(model_admin, name)
            elif hasattr(model, name):
                attr = getattr(model, name)
            elif form and name in form.fields:
                attr = form.fields[name]
            else:
                message = "Unable to lookup '%s' on %s" % (name, model._meta.object_name)
                if model_admin:
                    message += " or %s" % (model_admin.__class__.__name__,)
                if form:
                    message += " or %s" % form.__class__.__name__
                raise AttributeError(message)

            if hasattr(attr, "short_description"):
                label = attr.short_description
            elif (isinstance(attr, property) and
                  hasattr(attr, "fget") and
                  hasattr(attr.fget, "short_description")):
                label = attr.fget.short_description
            elif callable(attr):
                if attr.__name__ == "<lambda>":
                    label = "--"
                else:
                    label = utils.pretty_name(attr.__name__)
            else:
                label = utils.pretty_name(name)
    except utils.FieldIsAForeignKeyColumnName:
        label = utils.pretty_name(name)
        attr = name

    if return_attr:
        return (label, attr)
    else:
        return label
utils.label_for_field = label_for_field
