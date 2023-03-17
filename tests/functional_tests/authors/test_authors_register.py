import pytest
from parameterized import parameterized
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import AuthorsTestBase


def fill_form_dummy_data(form):
    fields = form.find_elements(By.TAG_NAME, 'input')

    for field in fields:
        if field.is_displayed():
            field.send_keys(' ' * 20)


@pytest.mark.functional_test
class AuthorsRegisterTest(AuthorsTestBase):

    def get_form(self):
        form_xpath = '/html/body/main/div[2]/form'

        return self.browser.find_element(By.XPATH, form_xpath)

    def form_field_test_with_callback(self, callback):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.get_form()

        fill_form_dummy_data(form)
        form.find_element(By.NAME, 'email').send_keys('dummy@email.com')

        callback(form)

        return form

    @parameterized.expand([
        ('Your username', 'This field must not be empty'),
        ('Ex.: John', 'Write your first name'),
        ('Ex.: Doe', 'Write your last name'),
        ('Type your password', 'Password must not be empty'),
        ('Repeat your password', 'Please, repeat your password')
    ])
    def test_empty_error_message(self, placeholder, msg):
        def callback(form):
            field = self.get_by_placeholder(form, placeholder)
            field.send_keys(' ')
            field.send_keys(Keys.ENTER)

            form = self.get_form()
            self.assertIn(msg, form.text)

        self.form_field_test_with_callback(callback)

    def test_invalid_email_error_message(self):
        def callback(form):
            email_field = self.get_by_placeholder(form, 'Your email')
            email_field.send_keys('email@invalid')
            email_field.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn('The e-mail must be valid.', form.text)

        self.form_field_test_with_callback(callback)

    def test_passwords_do_not_match(self):
        def callback(form):
            password1 = self.get_by_placeholder(form, 'Type your password')
            password2 = self.get_by_placeholder(form, 'Repeat your password')
            password1.send_keys('P@ssw0rd')
            password2.send_keys('P@ssw0rd_Different')
            password2.send_keys(Keys.ENTER)

            form = self.get_form()
            self.assertIn('Password and password2 must be equal', form.text)

        self.form_field_test_with_callback(callback)

    def test_user_valid_data_register_successfully(self):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.get_form()

        self.get_by_placeholder(form, 'Ex.: John').send_keys('First Name')
        self.get_by_placeholder(form, 'Ex.: Doe').send_keys('Last Name')
        self.get_by_placeholder(form, 'Your username').send_keys('my_username')
        self.get_by_placeholder(
            form, 'Your email').send_keys('email@valid.com')
        self.get_by_placeholder(
            form, 'Type your password').send_keys('P@ssw0rd1')
        self.get_by_placeholder(
            form, 'Repeat your password').send_keys('P@ssw0rd1')

        form.submit()

        self.assertIn(
            'Your user is created, please log in',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
