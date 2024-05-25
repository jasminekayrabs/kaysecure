from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class UserSecurityTests(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        self.user = User.objects.create_user(username='testuser', password='password123', email='user@example.com')

    def test_xss_protection(self):
        """
        Test that user inputs are escaped to prevent XSS attacks.
        """
        response = self.client.post(reverse('render_signup'), {
            'fname': '<script>alert("hack")</script>',
            'username': 'testuser',
            'email': 'user@example.com',
            'pass1': 'password123',
            'pass2': 'password123'
        }, follow=True)
        self.assertNotIn('<script>alert("hack")</script>', response.content.decode())

    def test_csrf_protection(self):
        """
        Ensure CSRF tokens are included in forms for protection.
        """
        response = self.client.get(reverse('render_signup'))
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_clickjacking_protection(self):
        """
        Ensure that the site is protected against clickjacking.
        """
        response = self.client.get(reverse('home'))
        self.assertEqual(response['X-Frame-Options'], 'DENY')

    def test_sql_injection(self):
        """
        Check robustness against SQL injection during login.
        """
        response = self.client.post(reverse('login'), {
            'username': 'admin\'--',
            'password': 'password123'
        })
        self.assertNotEqual(response.status_code, 200)
