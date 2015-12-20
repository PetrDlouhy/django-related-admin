# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import Album, Musician
from related_admin import RelatedFieldAdmin


class AlbumAdmin(RelatedFieldAdmin):
    list_display = ('name', 'artist__first_name', 'artist__last_name')


class MusicianAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')


admin.site.register(Album, AlbumAdmin)
admin.site.register(Musician, MusicianAdmin)
