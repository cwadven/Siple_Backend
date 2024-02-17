from django.test import TestCase
from django.urls import reverse


class HealthCheckViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse('common:health_check')

    def test_health_check_when_success(self):
        # Given:
        # When:
        response = self.client.get(self.url)

        # Then:
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'OK'})
