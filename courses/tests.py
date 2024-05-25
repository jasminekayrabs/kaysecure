from django.test import TestCase,  Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Course

class CourseViewTests(TestCase):
    def setUp(self):
        """
        Set up data for testing:
        - Creates a user account that can be used to authenticate in tests.
        - Creates a sample course that can be used in various tests.
        """
        # Create a user with a username and password
        self.user = User.objects.create_user(username='testuser', password='12345')
        # Create a sample course with a title and a description
        self.course = Course.objects.create(title='Test Course', description='Test Description')

    def test_course_content_view_redirect_if_not_logged_in(self):
        """
        Tests the course_content view to ensure it redirects a user to the login page
        if they are not logged in. This checks that the login_required decorator works.
        """
        # Construct the URL for the course_content view
        url = reverse('course_content', kwargs={'course_id': self.course.pk})
        # Make a GET request to the URL and capture the response
        response = self.client.get(url)
        # Assert that the response status code is 302, indicating a redirect
        self.assertEqual(response.status_code, 302)
        # Assert that the response redirects to the login page
        self.assertTrue('/accounts/login/' in response.url)

    def test_course_detail_view_with_nonexistent_course(self):
        """
        Tests the course_detail view to ensure it returns a 404 status code
        when a nonexistent course ID is requested. This checks the robustness of
        the view handling invalid inputs.
        """
        # Construct the URL for a nonexistent course ID
        url = reverse('course_detail', kwargs={'course_id': 999})
        # Make a GET request to the URL and capture the response
        response = self.client.get(url)
        # Assert that the response status code is 404, indicating the course was not found
        self.assertEqual(response.status_code, 404)

class SecurityTests(TestCase):
    def setUp(self):
        # Setting up a test user and course
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.course = Course.objects.create(title='Test Course', description='Safe <script>alert("test")</script> content')
        self.client = Client(enforce_csrf_checks=True)

    def test_xss_protection(self):
        """
        Test to ensure that user input is escaped,
        thus preventing XSS attacks.
        """
        response = self.client.get(reverse('course_detail', kwargs={'course_id': self.course.pk}))
        self.assertNotIn('<script>alert("test")</script>', response.content.decode())

    def test_clickjacking_protection(self):
        """
        Ensure that the X-Frame-Options header is set to DENY
        to protect against clickjacking.
        """
        response = self.client.get(reverse('course_detail', kwargs={'course_id': self.course.pk}))
        self.assertEqual(response['X-Frame-Options'], 'DENY')

def test_course_detail_view_protection(self):
    """
    test to check how the view handles non-integer strings for course_id that could still pass through URL pattern if not strictly integers.
    Ensure the course_detail view safely handles unexpected string inputs.
    """
    # Use a string that passes URL pattern but is clearly invalid
    malicious_course_id = '999999999'  # Assuming this ID does not exist
    response = self.client.get(reverse('course_detail', args=(malicious_course_id,)))
    self.assertEqual(response.status_code, 404, "Should return 404 for non-existent course ID")

    # Ensure regular usage works as expected
    response = self.client.get(reverse('course_detail', args=(self.course.pk,)))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, self.course.title)
