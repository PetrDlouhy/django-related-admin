# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import Album, Musician, Concert
from related_admin import RelatedFieldAdmin
from django.core.urlresolvers import reverse
from cgi import escape


class AlbumAdmin(RelatedFieldAdmin):
    list_display = ('name', 'artist__first_name', 'artist__last_name')


class MusicianAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')


class ConcertAdmin(RelatedFieldAdmin):
    list_display = ('name', 'main_performer_link')
    list_select_related = ('main_performer',)

    def main_performer_link(self, obj):
        url = reverse("admin:main_musician_change", args=[obj.main_performer.id])
        return '<a href="%s">%s</a>' % (url, escape(str(obj)))
    main_performer_link.allow_tags = True
    main_performer_link.short_description = "Main performer"

admin.site.register(Album, AlbumAdmin)
admin.site.register(Musician, MusicianAdmin)
admin.site.register(Concert, ConcertAdmin)
