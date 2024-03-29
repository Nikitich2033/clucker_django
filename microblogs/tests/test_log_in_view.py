from django.test import TestCase
from django.urls import reverse
from microblogs.forms import LogInForm
from microblogs.models import User
from django.contrib.auth.hashers import check_password
from .helpers import LogInTester
from django.contrib import messages

class LogInViewTestCase(TestCase, LogInTester):

    def setUp(self):
        self.url = reverse('log_in')
        self.user = User.objects.create_user(
            '@johndoe',
            first_name = 'John',
            last_name = 'Doe',
            email = 'johndoe@example.org',
            password = 'Password123',
            bio = 'my name john',
            is_active = True
        )

    def test_sign_up_url(self):
        self.assertEqual(self.url,'/log_in/')

    def test_get_log_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)

    def test_unsuccessful_log_in(self):
        form_input = {'username':'@johndoe','password':'WrongPassword123'}
        response = self.client.post(self.url,form_input)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(self._is_logged_in())
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level,messages.ERROR)

    def test_successful_log_in(self):
        form_input = {'username':'@johndoe','password':'Password123'}
        response = self.client.post(self.url,form_input, follow = True)
        self.assertTrue(self._is_logged_in())
        response_url = reverse('feed')
        self.assertRedirects(response, response_url,status_code=302,target_status_code = 200)
        self.assertTemplateUsed(response,'feed.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)

    def test_valid_log_in_by_inactive_user(self):
        self.user.is_active = False
        self.user.save()
        form_input = {'username':'@johndoe','password':'Password123'}
        response = self.client.post(self.url,form_input, follow = True)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(self._is_logged_in())
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level,messages.ERROR)
