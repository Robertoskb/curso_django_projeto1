from unittest import TestCase

from django.test import TestCase as DjangoTestCase
from django.urls import reverse
from parameterized import parameterized

from authors.forms import RegisterForm


class AuthorRegisterFormUnitTest(TestCase):

    @parameterized.expand([
        ('username', 'Your username'),
        ('email', 'Your email'),
        ('first_name', 'Ex.: John'),
        ('last_name', 'Ex.: Doe'),
        ('password', 'Type your password'),
        ('password2', 'Repeat your password'),
    ])
    def test_fields_placeholder(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']

        self.assertEqual(current_placeholder, placeholder)

    @parameterized.expand([
        ('email', 'The e-mail must be valid.'),
        ('password', (
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        )),
    ])
    def test_fields_help_text(self, field, help_text):
        form = RegisterForm()
        current_help_text = form[field].field.help_text

        self.assertEqual(current_help_text, help_text)

    @parameterized.expand([
        ('username', 'Username'),
        ('first_name', 'First name'),
        ('last_name', 'Last name'),
        ('email', 'E-mail'),
        ('password', 'Password'),
        ('password2', 'Password2')
    ])
    def test_fields_label(self, field, label):
        form = RegisterForm()
        current_label = form[field].field.label

        self.assertEqual(current_label, label)


class AuthorRegisterFormIntergrationTest(DjangoTestCase):
    def setUp(self) -> None:
        self.form_data = {
            'username': 'username',
            'first_name': 'User',
            'last_name': 'Name',
            'email': 'user@anyemail.com',
            'password': 'Passw0rd1',
            'password2': 'Passw0rd1',
        }

        return super().setUp()

    @parameterized.expand([
        ('username', 'This field must not be empty'),
        ('first_name', 'Write your first name'),
        ('last_name', 'Write your last name'),
        ('email', 'Write your e-mail'),
        ('password', 'Password must not be empty'),
        ('password2', 'Please, repeat your password')
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''

        response = self.client.post(reverse('authors:register_create'),
                                    data=self.form_data, follow=True)

        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get(field))

    def test_passwords_cannot_be_different(self):
        self.form_data['password2'] = 'Str0ngP@ssword2'

        response = self.client.post(
            reverse('authors:register_create'),
            data=self.form_data, follow=True)

        msg = 'Password and password2 must be equal'
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('password'))

    def test_password_cannot_be_weak(self):
        self.form_data['password'] = 'weak_password'

        response = self.client.post(
            reverse('authors:register_create'),
            data=self.form_data, follow=True)

        msg = (
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.')

        self.assertIn(msg, response.context['form'].errors.get('password'))

    def test_author_create_view_returns_sucess_mensge_if_form_is_valid(self):
        response = self.client.post(reverse('authors:register_create'),
                                    data=self.form_data, follow=True)

        self.assertIn('Your user is created, please log in',
                      response.content.decode('utf-8'))

    def test_username_field_min_length_should_be_4(self):
        self.form_data['username'] = 'use'

        response = self.client.post(
            reverse('authors:register_create'),
            data=self.form_data, follow=True)

        msg = 'Username must have at least 4 characters'

        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))

    def test_username_field_max_length_should_be_150(self):
        self.form_data['username'] = 'a'*151

        response = self.client.post(
            reverse('authors:register_create'),
            data=self.form_data, follow=True)

        msg = 'Username must have less than 150 characters'

        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))

    def test_email_already_exists(self):
        self.client.post(reverse('authors:register_create'),
                         data=self.form_data)
        self.form_data['username'] = 'otherusername'

        response = self.client.post(
            reverse('authors:register_create'),
            data=self.form_data, follow=True)

        msg = 'Email already in use'

        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('email'))

    def test_author_created_can_login(self):
        url = reverse('authors:register_create')
        data = self.form_data
        self.client.post(url, data=data)

        is_authenticated = self.client.login(
            username=data['username'], password=data['password'])

        self.assertTrue(is_authenticated)
