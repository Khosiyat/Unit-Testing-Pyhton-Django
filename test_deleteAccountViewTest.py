from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

class DeleteAccountViewTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_delete_account_authenticated_user(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Simulate a GET request to delete the user account
        url = reverse('delete_account')
        response = self.client.get(url)

        # Check if the response is a redirect to the signup page
        self.assertRedirects(response, reverse('signup'))

        # Check if the user account has been deleted
        self.assertFalse(User.objects.filter(username='testuser').exists())

    def test_delete_account_unauthenticated_user(self):
        # Log out the user (unauthenticated)
        self.client.logout()

        # Simulate a GET request to delete the user account
        url = reverse('delete_account')
        response = self.client.get(url)

        # Check if the response is a redirect to the signup page (for unauthenticated users)
        self.assertRedirects(response, reverse('signup'))

        # Check if the user account still exists (no deletion for unauthenticated users)
        self.assertTrue(User.objects.filter(username='testuser').exists())
