from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from sign.models import Event, Guest


class ModelTest(TestCase):
    def setUp(self):
        Event.objects.create(id=1, name="oneplus 3 event", status=True, limit=2000, address='shenzhen', start_time='2016-08-31 02:18:22')
        Guest.objects.create(id=1, event_id=1, realname='alen', phone='11111111110', email='alen@mail.com', sign=False)

    def test_event_models(self):
        result = Event.objects.get(name="oneplus 3 event")
        self.assertEqual(result.address, "beijing")
        self.assertTrue(result.status)

    def test_guest_models(self):
        result = Guest.objects.get(phone='11111111110')
        self.assertEquals(result.realname, 'alen')
        self.assertFalse(result.sign)

class IndexPageTest(TestCase):
    def test_index_page_renders_index_template(self):
        response = self.client.get('/sign/index.html')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sign/index.html')

class LoginActionTest(TestCase):
    def setUp(self):
        user = User.objects.create_user('admin', 'admin@mail.com', 'admin123456')
        self.assertEqual(user.username, "admin")
        self.assertEqual(user.email, "admin@mail.com")

    def test_login_action_username_password_null(self):
       test_data = {'username': '', 'password': ''}
       response = self.client.post('/sign/login_action', data=test_data)
       self.assertEqual(response.status_code, 200)
       self.assertIn(b"username or password error!", response.content)

    def test_login_action_username_password_error(self):
       test_data = {'username': 'abcd', 'password': '1234'}
       response = self.client.post('/sign/login_action', data=test_data)
       self.assertEqual(response.status_code, 200)
       self.assertIn(b"username or password error!", response.content)

    def test_login_action_success(self):
       test_data = {'username': 'admin', 'password': 'admin123456'}
       response = self.client.post('/sign/login_action', data=test_data)
       self.assertEqual(response.status_code, 302)


