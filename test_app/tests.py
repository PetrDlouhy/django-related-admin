from django.test import TestCase, RequestFactory
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

    def test_admin_views_list_select_related_competition(self):
        self.assertTrue(self.client.login(username='admin', password='admin'))
        response = self.client.get(reverse("admin:main_concert_changelist"))
        self.assertEqual(response.status_code, 200)
