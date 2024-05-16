from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse


class FoodgramAPITestCase(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_list_exists(self):
        """Проверка доступности списка тегов."""
        url = reverse('tag-list')
        response = self.guest_client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
