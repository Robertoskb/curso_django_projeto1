from django.test import TestCase
from django.urls import resolve, reverse

from authors import views


class AuthorsCreateViewTest(TestCase):

    def test_authors_create_view_function_is_correct(self):
        view = resolve(reverse('authors:register_create'))

        self.assertEqual(view.func, views.register_create)

    def test_author_create_view_raises_404_if_not_post(self):
        response = self.client.get(reverse('authors:register_create'))

        self.assertEqual(response.status_code, 404)
