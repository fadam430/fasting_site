from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class RegistrationRedirectTests(TestCase):
    def test_register_redirects_to_allauth_signup(self):
        """GET /fasting/register/ should redirect to /accounts/signup/"""
        response = self.client.get('/fasting/register/')
        self.assertEqual(response.status_code, 302)
        # Location can be absolute (http://testserver/accounts/signup/) so assert substring
        self.assertIn('/accounts/signup/', response['Location'])


class AuthPagesTests(TestCase):
    def test_login_page_loads(self):
        """The allauth login page is accessible and renders the password field."""
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)
        # Ensure the login form contains a password input
        self.assertContains(response, 'name="password"')

    def test_signup_creates_user(self):
        """Posting the signup form creates a user in the database."""
        data = {
            'username': 'testuser',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!',
        }
        response = self.client.post('/accounts/signup/', data)
        # Allauth redirects on successful signup
        self.assertIn(response.status_code, (302, 303))
        self.assertTrue(User.objects.filter(username='testuser').exists())


class AuthFlowTests(TestCase):
    def test_login_and_logout_flow(self):
        """A user can log in and then log out (session is cleared)."""
        username = 'flowuser'
        password = 'StrongPass123!'
        User.objects.create_user(username=username, password=password)

        # Login via allauth login form
        login_resp = self.client.post('/accounts/login/', {'login': username, 'password': password})
        self.assertIn(login_resp.status_code, (302, 303))

        # After login, subsequent requests see the user as authenticated
        home_resp = self.client.get('/')
        self.assertTrue(home_resp.context['user'].is_authenticated)

        # Logout (GET — configured to logout on GET)
        logout_resp = self.client.get('/accounts/logout/')
        # should redirect home
        self.assertIn(logout_resp.status_code, (302, 303))
        # Ensure the user is no longer authenticated
        home_after = self.client.get('/')
        self.assertFalse(home_after.context['user'].is_authenticated)

    def test_add_review_requires_login(self):
        """Posting to the add_review URL when anonymous should redirect to login."""
        # Use a sample POST; login_required should redirect before examining POST data
        resp = self.client.post('/fasting/review/add/', {'plan_id': 1, 'rating': 5, 'comment': 'Nice'})
        self.assertEqual(resp.status_code, 302)
        self.assertIn('/accounts/login/', resp['Location'])

