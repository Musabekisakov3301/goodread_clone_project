from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user

from users.models import CustomUser

class RegistrationTestCase(TestCase):
    def test_user_account_is_created(self):
        self.client.post(
            reverse('users:register'),
            data={
                'username': 'testuser',
                'first_name': 'musabek',
                'last_name': 'isakov',
                'email': 'musabekisakov5@gmail.com',
                'password': 'musabekisakov7346436'
            }
        )

        user = CustomUser.objects.get(username='testuser')

        self.assertEqual(user.first_name, 'musabek')
        self.assertEqual(user.last_name, 'isakov')
        self.assertEqual(user.email, 'musabekisakov5@gmail.com')
        self.assertNotEqual(user.password, 'musabekisakov7346436')
        self.assertTrue(user.check_password('musabekisakov7346436'))
    
    def test_required_fields(self): 
        response = self.client.post(
            reverse('users:register'),
            data={
                'first_name': 'musabek',
                'email': 'musabekisakov5@gmail.com'
            }
        )

        user_count = CustomUser.objects.count()

        self.assertEqual(user_count, 0)
        self.assertFormError(response, 'form', 'username', 'This field is required.')
        self.assertFormError(response, 'form', 'password', 'This field is required.')
    
    def test_invalid_email(self):
        response = self.client.post(
            reverse('users:register'),
            data={
                'username': 'testuser',
                'first_name': 'musabek',
                'last_name': 'isakov',
                'email': 'email',
                'password': 'musabekisakov7346436'
            }
        )
         
        user_count = CustomUser.objects.count()

        self.assertEqual(user_count, 0)
        self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')

    def test_unique_username(self):

        user = CustomUser.objects.create(username='testuser', first_name='musabek1')
        user.set_password('123456789')
        user.save()
        
        response = self.client.post(
            reverse('users:register'),
            data={
                'username': 'testuser',
                'first_name': 'musabek',
                'last_name': 'isakov',
                'email': 'email',
                'password': 'musabekisakov7346436'
            }
        )

        user_count = CustomUser.objects.count()

        self.assertEqual(user_count, 1)


        self.assertFormError(response, 'form', 'username', 'A user with that username already exists.')

class LoginTestCase(TestCase):
    # DRY - Don't repeat yourself
    def setUp(self):
        self.db_user = CustomUser.objects.create(username='musabek', first_name='musabek')
        self.db_user.set_password('123456789')
        self.db_user.save()


    def test_successful_login(self):
        self.client.post(
            reverse('users:login'),
            data={
                'username': 'musabek',
                'password': '123456789'
            }
        )

        user = get_user(self.client)

        self.assertTrue(user.is_authenticated)

    def test_wrong_credentials(self):
        self.client.post(
            reverse('users:login'),
            data={
                'username': 'user',
                'password': '123456789'
            }
        )

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

        self.client.post(
            reverse('users:login'),
            data={
                'username': 'musabek',
                'password': 'password'
            }
        )

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)
    
    def test_logout(self):
        self.client.login(username='musabek', password='123456789')

        self.client.get(reverse('users:logout'))
        
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

class ProfileTestCase(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse('users:profile'))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('users:login') + '?next=/users/profile/')
    
    def test_profile_details(self):
        user = CustomUser.objects.create(
            username='user1', first_name='user_first_name', last_name='user_last_name', email='musabekisakov5@gmail.com'
        )
        user.set_password('123456789')
        user.save()

        self.client.login(username='user1', password='123456789')

        response = self.client.get(reverse('users:profile'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user.username)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.email)

    def test_update_profile(self):
        user = CustomUser.objects.create(
            username='user1', first_name='user_first_name', last_name='user_last_name', email='musabekisakov5@gmail.com'
        )
        user.set_password('123456789')
        user.save()

        self.client.login(username='user1', password='123456789')

        response = self.client.post(
            reverse('users:profile-edit'),
            data={
                'username': 'user1',
                'first_name': 'user_first_name',
                'last_name': 'user_last_name_2',
                'email': 'musabekisakov@gmail.com'
            }
        )
        #1 
        user = CustomUser.objects.get(pk=user.pk)
        #2 
        #user.refresh_from_db()

        self.assertEqual(user.last_name, 'user_last_name_2')
        self.assertEqual(user.email, 'musabekisakov@gmail.com')
        self.assertEqual(response.url, reverse('users:profile'))