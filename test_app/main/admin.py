# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.html import format_html

from related_admin import RelatedFieldAdmin, getter_for_related_field
try:
    from django.urls import reverse
except ImportError:  # for Django<1.9
    from django.core.urlresolvers import reverse
try:
    from html import escape
except ImportError:  # for Python < 3.0
    from cgi import escape

from .models import Album, Concert, Musician


class AlbumAdmin(RelatedFieldAdmin):
    list_display = ('name', 'artist__first_name', 'artist__last_name', 'artist__full_name', 'artist__active')

    artist__active = getter_for_related_field('artist__active', boolean=True)


class MusicianAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')


class ConcertAdmin(RelatedFieldAdmin):
    list_display = ('name', 'main_performer_link')
    list_select_related = ('main_performer',)

    def main_performer_link(self, obj):
        url = reverse("admin:main_musician_change", args=[obj.main_performer.id])
        return format_html('<a href="%s">{}</a>', (url, escape(str(obj))))
    main_performer_link.short_description = "Main performer"


admin.site.register(Album, AlbumAdmin)
admin.site.register(Musician, MusicianAdmin)
admin.site.register(Concert, ConcertAdmin)
