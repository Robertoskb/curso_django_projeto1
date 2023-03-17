from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AuhtorLogoutTest(TestCase):

    def test_user_tries_to_logout_using_get_method(self):
        data = {'username': 'my_user', 'password': 'my_password'}
        User.objects.create_user(**data)
        self.client.login(**data)

        response = self.client.get(reverse('authors:logout'), follow=True)
        self.assertIn('Invalid logout request',
                      response.content.decode('utf-8'))

    def test_user_tries_to_logout_another_user(self):
        data = {'username': 'my_user', 'password': 'my_password'}
        User.objects.create_user(**data)
        self.client.login(**data)

        response = self.client.post(reverse('authors:logout'),
                                    data={'username': 'another_user',
                                          'password': 'my_password'},
                                    follow=True)

        self.assertIn('Invalid logout user',
                      response.content.decode('utf-8'))

    def test_user_can_logout_successfully(self):
        data = {'username': 'my_user', 'password': 'my_password'}
        User.objects.create_user(**data)
        self.client.login(**data)

        response = self.client.post(
            reverse('authors:logout'), follow=True, data=data)
        self.assertIn('Logged out successfully',
                      response.content.decode('utf-8'))
