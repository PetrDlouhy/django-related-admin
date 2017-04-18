import django
from django.contrib.admin.utils import display_for_field as django_display_for_field


if django.VERSION >= (1, 9):
    def get_empty_value_display(model_admin):
        return model_admin.get_empty_value_display()

    display_for_field = django_display_for_field
else:
    def get_empty_value_display(model_admin):
        from django.contrib.admin.views.main import EMPTY_CHANGELIST_VALUE
        return EMPTY_CHANGELIST_VALUE

    def display_for_field(value, field, empty_value_display):
        if value is None:
            return empty_value_display
        else:
            return django_display_for_field(value, field)
