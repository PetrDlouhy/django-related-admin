from django.contrib.admin.templatetags.admin_list import _boolean_icon
from django.test import RequestFactory, TestCase

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
