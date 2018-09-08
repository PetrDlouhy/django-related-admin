# -*- coding: utf-8 -*-
from django.db import models

INSTRUMENTS_CHOICES = (
    ('GUITAR', 'Guitar'),
    ('VOICE', 'Voice'),
    ('DRUM', 'Drum'),
    ('SAX', 'Saxophone'),
)


class Musician(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    instrument = models.CharField(choices=INSTRUMENTS_CHOICES, max_length=100)
    active = models.BooleanField(default=True)

    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def __str__(self):
        return self.full_name()

    def is_on_tour(self):
        return self.active


class Album(models.Model):
    artist = models.ForeignKey(Musician, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    release_date = models.DateField()


class Concert(models.Model):
    name = models.CharField(max_length=100)
    main_performer = models.ForeignKey(Musician, on_delete=models.CASCADE)
