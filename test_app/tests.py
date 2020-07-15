import datetime
from unittest.mock import MagicMock

from django.contrib.admin import AdminSite, ModelAdmin
from django.contrib.admin.templatetags.admin_list import _boolean_icon
from django.db import models
from django.test import RequestFactory, TestCase

from related_admin import RelatedFieldAdmin

from test_app.main.models import INSTRUMENTS_CHOICES
try:
    from django.urls import reverse
except ImportError:  # for Django<1.10
    from django.core.urlresolvers import reverse


class AdminFilterTests(TestCase):
    fixtures = ['data']

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.assertTrue(self.client.login(username='admin', password='admin'))

    def test_musician_view_choices(self):
        response = self.client.get(reverse("admin:main_musician_changelist"))
        self.assertContains(response, '<td class="field-instrument">%s</td>' % dict(INSTRUMENTS_CHOICES)['VOICE'], html=True)

    def test_admin_views_competition(self):
        response = self.client.get(reverse("admin:main_album_changelist"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            '<th scope="col"  class="sortable column-artist__first_name">'
            '<div class="text"><a href="?o=3">Artist First Name</a></div>'
            '<div class="clear"></div>'
            '</th>',
            html=True,
        )
        self.assertContains(response, '<td class="field-artist__full_name">Mark Knopfler</td>', html=True)
        self.assertContains(response, '<td class="field-artist__active">%s</td>' % _boolean_icon(True), html=True)
        self.assertContains(response, '<td class="field-artist__instrument">%s</td>' % dict(INSTRUMENTS_CHOICES)['VOICE'], html=True)

    def test_admin_views_list_select_related_competition(self):
        response = self.client.get(reverse("admin:main_concert_changelist"))
        self.assertContains(response, '<td class="field-main_performer__is_on_tour">%s</td>' % _boolean_icon(True), html=True)
        self.assertEqual(response.status_code, 200)


class TestModelFieldAdmin(ModelAdmin):
    fake_qs = MagicMock()

    def get_queryset(self, request):
        return self.fake_qs


class TestRelatedFieldAdmin(RelatedFieldAdmin, TestModelFieldAdmin):
    pass


class RelatedFieldAdminTests(TestCase):
    def test_related_field(self):
        class Musician(models.Model):
            first_name = models.CharField(max_length=50)

            class Meta:
                app_label = 'test'

        class Album(models.Model):
            artist = models.ForeignKey(Musician, on_delete=models.CASCADE, null=True, blank=True)

            class Meta:
                app_label = 'test'

        class TestAdmin(TestRelatedFieldAdmin):
            list_display = ('artist__first_name',)

        admin = TestAdmin(Album, AdminSite())
        album = Album(artist=Musician(first_name='Foo'))
        self.assertEqual(admin.artist__first_name(album), 'Foo')
        self.assertEqual(admin.get_list_display(None), ('artist__first_name',))

        admin.get_queryset(None)
        admin.fake_qs.select_related.assert_called_with('artist')

    def test_callable_field(self):
        class Musician1(models.Model):
            def get_foo(self):
                return 'Foo'

            class Meta:
                app_label = 'test'

        class Album1(models.Model):
            artist = models.ForeignKey(Musician1, on_delete=models.CASCADE, null=True, blank=True)

            class Meta:
                app_label = 'test'

        class TestAdmin(TestRelatedFieldAdmin):
            list_display = ('artist__get_foo',)

        admin = TestAdmin(Album1, AdminSite())
        album = Album1(artist=Musician1())
        self.assertEqual(admin.artist__get_foo(album), 'Foo')
        self.assertEqual(admin.get_list_display(None), ('artist__get_foo',))

        admin.get_queryset(None)
        admin.fake_qs.select_related.assert_called_with('artist')

    def test_date_field_filter(self):
        class Musician2(models.Model):
            birthday = models.DateField()

            class Meta:
                app_label = 'test'

        class Album2(models.Model):
            artist = models.ForeignKey(Musician2, on_delete=models.CASCADE, null=True, blank=True)

            class Meta:
                app_label = 'test'

        class TestAdmin(TestRelatedFieldAdmin):
            list_display = ('artist__birthday__month',)

        admin = TestAdmin(Album2, AdminSite())
        artist = Musician2(birthday=datetime.date(2020, 2, 2))
        self.assertEqual(admin.artist__birthday__month(Album2(artist=artist)), 2)
        self.assertEqual(admin.get_list_display(None), ('artist__birthday__month',))

        admin.get_queryset(None)
        admin.fake_qs.select_related.assert_called_with()

    def test_list_select_related_field(self):
        """ Test, that list_select_related is preserved for select_related in queryset """
        class Musician3(models.Model):
            def get_foo(self):
                return 'Foo'

            class Meta:
                app_label = 'test'

        class Album3(models.Model):
            artist = models.ForeignKey(Musician3, on_delete=models.CASCADE, null=True, blank=True)

            class Meta:
                app_label = 'test'

        class TestAdmin(TestRelatedFieldAdmin):
            list_display = ('artist__get_foo',)
            list_select_related = ('artist', )

        admin = TestAdmin(Album3, AdminSite())
        album = Album3(artist=Musician3())
        self.assertEqual(admin.artist__get_foo(album), 'Foo')
        self.assertEqual(admin.get_list_display(None), ('artist__get_foo',))

        admin.get_queryset(None)
        admin.fake_qs.select_related.assert_called_with('artist', 'artist')

    def test_list_select_related_true_field(self):
        """ Test, that list_select_related=True works """
        class Musician4(models.Model):
            def get_foo(self):
                return 'Foo'

            class Meta:
                app_label = 'test'

        class Album4(models.Model):
            artist = models.ForeignKey(Musician4, on_delete=models.CASCADE, null=True, blank=True)

            class Meta:
                app_label = 'test'

        class TestAdmin(TestRelatedFieldAdmin):
            list_display = ('artist__get_foo',)
            list_select_related = True

        admin = TestAdmin(Album4, AdminSite())
        album = Album4(artist=Musician4())
        self.assertEqual(admin.artist__get_foo(album), 'Foo')
        self.assertEqual(admin.get_list_display(None), ('artist__get_foo',))

        admin.get_queryset(None)
        admin.fake_qs.select_related.assert_called_with('artist')

    def test_list_select_related_fields_cascade(self):
        """ Test, that cascade of foreign keys correctly fetches fields through select_related """
        class Musician5(models.Model):
            first_name = models.CharField(max_length=50)

            class Meta:
                app_label = 'test'

        class Album5(models.Model):
            artist = models.ForeignKey(Musician5, on_delete=models.CASCADE, null=True, blank=True)

            class Meta:
                app_label = 'test'

        class Set5(models.Model):
            album = models.ForeignKey(Album5, on_delete=models.CASCADE)

            class Meta:
                app_label = 'test'

        class TestAdmin(TestRelatedFieldAdmin):
            list_display = ('album__artist__first_name', 'album')
            list_select_related = True

        admin = TestAdmin(Set5, AdminSite())
        set5 = Set5(album=Album5(artist=Musician5(first_name='Foo name')))
        self.assertEqual(admin.album__artist__first_name(set5), 'Foo name')
        self.assertEqual(admin.get_list_display(None), ('album__artist__first_name', 'album'))

        admin.fake_qs.model = Set5
        admin.get_queryset(None)
        admin.fake_qs.select_related.assert_called_with('album__artist', 'album')

    def test_methods_as_feilds(self):
        """ Test, if method is used as field """
        class Musician6(models.Model):
            class Meta:
                app_label = 'test'

        class TestAdmin(TestRelatedFieldAdmin):
            def get_foo(self):
                return 'Foo'

            list_display = (get_foo,)

        admin = TestAdmin(Musician6, AdminSite())
        self.assertEqual(admin.get_foo(), 'Foo')
        self.assertEqual(admin.get_list_display(None), (TestAdmin.get_foo,))

        admin.get_queryset(None)
        admin.fake_qs.select_related.assert_called_with()
