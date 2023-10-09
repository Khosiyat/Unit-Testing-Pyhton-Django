from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class UserAccountManagementIntegrationTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_user_account_management_flow(self):
        # Simulate user registration
        response = self.client.post(reverse('signup'), data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword',
        })

        # Check if the user is redirected to the index page after registration
        self.assertRedirects(response, reverse('index'))

        # Check if the new user account exists
        self.assertTrue(User.objects.filter(username='newuser').exists())

        # Log in the new user
        self.client.login(username='newuser', password='newpassword')

        # Simulate changing the user's password
        response = self.client.post(reverse('change_password'), data={
            'new_password': 'newpassword123',
        })

        # Check if the user is redirected to the password change done page
        self.assertRedirects(response, reverse('change_password_done'))

        # Log out the user
        self.client.logout()

        # Simulate deleting the user account
        response = self.client.get(reverse('delete_account'))

        # Check if the user is redirected to the signup page after account deletion
        self.assertRedirects(response, reverse('signup'))

        # Check if the user account has been deleted
        self.assertFalse(User.objects.filter(username='newuser').exists())
