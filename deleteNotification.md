from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Notification

class DeleteNotificationViewTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        # Create a test notification for the user
        self.notification = Notification.objects.create(user=self.user, message='Test notification')

    def test_delete_notification(self):
        # Get the initial count of notifications for the user
        initial_count = Notification.objects.filter(user=self.user).count()

        # Simulate a GET request to delete the notification
        url = reverse('delete_notification', args=[self.notification.id])
        response = self.client.get(url)

        # Check if the response is a redirect to the index page
        self.assertRedirects(response, reverse('index'))

        # Check if the notification has been deleted
        self.assertEqual(Notification.objects.filter(user=self.user).count(), initial_count - 1)

    def test_delete_nonexistent_notification(self):
        # Get the initial count of notifications for the user
        initial_count = Notification.objects.filter(user=self.user).count()

        # Simulate a GET request to delete a nonexistent notification
        url = reverse('delete_notification', args=[999])  # Using a nonexistent notification ID
        response = self.client.get(url)

        # Check if the response is a redirect to the index page
        self.assertRedirects(response, reverse('index'))

        # Check if the count of notifications remains the same
        self.assertEqual(Notification.objects.filter(user=self.user).count(), initial_count)
