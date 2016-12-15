from django.contrib.admin.templatetags.admin_list import _boolean_icon
from django.test import RequestFactory, TestCase
try:
    from django.urls import reverse
except ImportError:  # for Django<1.10
    from django.core.urlresolvers import reverse


class AdminFilterTests(TestCase):
    fixtures = ['data']

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    def test_admin_views_competition(self):
        self.assertTrue(self.client.login(username='admin', password='admin'))
        response = self.client.get(reverse("admin:main_album_changelist"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<td class="field-artist__full_name">Mark Knopfler</td>', html=True)
        self.assertContains(response, '<td class="field-artist__active">%s</td>' % _boolean_icon(True), html=True)

    def test_admin_views_list_select_related_competition(self):
        self.assertTrue(self.client.login(username='admin', password='admin'))
        response = self.client.get(reverse("admin:main_concert_changelist"))
        self.assertEqual(response.status_code, 200)
