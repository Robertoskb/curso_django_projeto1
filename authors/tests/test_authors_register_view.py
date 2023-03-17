from django.test import TestCase
from django.urls import resolve, reverse

from authors import views


class AuthorsRegisterViewTest(TestCase):

    def test_authors_register_view_function_is_correct(self):
        view = resolve(reverse('authors:register'))

        self.assertEqual(view.func, views.register_view)

    def test_authors_register_view_template_is_correct(self):
        response = self.client.get(reverse('authors:register'))

        self.assertTemplateUsed(response, 'authors/pages/register_view.html')
