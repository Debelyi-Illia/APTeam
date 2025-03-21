from django.test import TestCase, Client
from django.urls import reverse
from myapp.models import User, Advertisement
from myapp.forms import CustomUserCreationForm
from django.utils import timezone
from datetime import timedelta


class LoginTests(TestCase):
    def setUp(self):
        # Тестовий користувач
        self.client = Client()
        self.login_url = reverse('login')
        self.test_user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User',
        )

    def test_login_page_loads(self):
        """Перевірка завантаження сторінки входу"""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_successful_login(self):
        """Перевірка успішного входу з правильними обліковими даними"""
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertRedirects(response, reverse('user_profile'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_failed_login_wrong_password(self):
        """Перевірка невдалого входу з неправильним паролем"""
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_failed_login_nonexistent_user(self):
        """Перевірка невдалого входу з неіснуючим користувачем"""
        response = self.client.post(self.login_url, {
            'username': 'nonexistentuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_login_form_empty_fields(self):
        """Перевірка форми входу з порожніми полями"""
        response = self.client.post(self.login_url, {
            'username': '',
            'password': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_logout(self):
        """Перевірка функціональності виходу з системи"""
        login_response = self.client.login(username='testuser', password='testpass123')
        self.assertTrue(login_response)
        
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('home'))
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_login_redirect_authenticated_user(self):
        """Перевірка перенаправлення авторизованих користувачів зі сторінки входу"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.login_url)
        self.assertRedirects(response, reverse('user_profile'))

class SearchTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.search_url = reverse('search')
        self.test_user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User',
        )
        self.ad1 = Advertisement.objects.create(
            ad_poster=self.test_user,
            ad_title='Ad Title 1',
            ad_role='Mentor',
            ad_text_body='This is the body of ad 1',
            ad_subject='Subject 1',
            ad_start_time=timezone.now(),
            ad_end_time=timezone.now() + timedelta(days=1),
            is_active=True,
        )
        self.ad2 = Advertisement.objects.create(
            ad_poster=self.test_user,
            ad_title='Ad Title 2',
            ad_role='Mentee',
            ad_text_body='This is the body of ad 2',
            ad_subject='Subject 2',
            ad_start_time=timezone.now(),
            ad_end_time=timezone.now() + timedelta(days=1),
            is_active=True,
        )

    def test_search_advertisements(self):
        """Перевірка функціональності пошуку"""
        response = self.client.get(self.search_url, {'query': 'body of ad 1'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This is the body of ad 1')
        self.assertNotContains(response, 'This is the body of ad 2')

    def test_search_advertisements_by_role(self):
        """Перевірка функціональності пошуку з фільтром за роллю"""
        response = self.client.get(self.search_url, {'role': 'Mentee'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This is the body of ad 1')
        self.assertNotContains(response, 'This is the body of ad 2')

class RegisterViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')

    def test_register_page_loads(self):
        """Перевірка завантаження сторінки реєстрації"""
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.assertIsInstance(response.context['form'], CustomUserCreationForm)

    def test_successful_registration(self):
        """Перевірка успішної реєстрації з правильними даними"""
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'first_name': 'New',
            'last_name': 'User',
        })
        self.assertRedirects(response, reverse('user_profile'))
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_registration_with_empty_username(self):
        """Перевірка реєстрації з порожнім ім'ям користувача"""
        response = self.client.post(self.register_url, {
            'username': '',
            'email': 'newuser@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'first_name': 'New',
            'last_name': 'User',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.assertFalse(User.objects.filter(email='newuser@example.com').exists())
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_registration_with_invalid_email(self):
        """Перевірка невдалої реєстрації з неправильною електронною адресою"""
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'email': 'invalidemail',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'first_name': 'New',
            'last_name': 'User',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.assertFalse(User.objects.filter(username='newuser').exists())
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_registration_with_password_mismatch(self):
        """Перевірка невдалої реєстрації з різними паролями"""
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'testpass123',
            'password2': 'differentpass',
            'first_name': 'New',
            'last_name': 'User',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.assertFalse(User.objects.filter(username='newuser').exists())
        self.assertFalse(response.wsgi_request.user.is_authenticated)
    
    def test_registration_with_empty_password(self):
        """Перевірка невдалої реєстрації з порожніми паролями"""
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': '',
            'password2': '',
            'first_name': 'New',
            'last_name': 'User',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.assertFalse(User.objects.filter(username='newuser').exists())
        self.assertFalse(response.wsgi_request.user.is_authenticated)