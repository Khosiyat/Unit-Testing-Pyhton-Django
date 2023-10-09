from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Notification, Profile

class UserProfileAndNotificationsIntegrationTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_user_profile_and_notifications_flow(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Simulate a GET request to view the user's profile
        url = reverse('profile', args=['testuser'])
        response = self.client.get(url)

        # Check if the response contains the user's profile information
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'User Profile')

        # Simulate sending a notification to the user
        self.client.post(reverse('send_notification'), data={'recipient': 'testuser', 'message': 'Test notification'})

        # Check if the notification was sent
        self.assertTrue(Notification.objects.filter(user=self.user, message='Test notification').exists())

        # Simulate viewing notifications
        response = self.client.get(reverse('view_notifications'))

        # Check if the response contains the notification
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test notification')

        # Simulate deleting the notification
        notification_id = Notification.objects.get(user=self.user, message='Test notification').id
        self.client.get(reverse('delete_notification', args=[notification_id]))

        # Check if the notification has been deleted
        self.assertFalse(Notification.objects.filter(id=notification_id).exists())

        # Simulate updating the user's profile
        self.client.post(reverse('edit_profile'), data={'first_name': 'Updated', 'last_name': 'Profile'})

        # Check if the user's profile information has been updated
        updated_profile = Profile.objects.get(user=self.user)
        self.assertEqual(updated_profile.first_name, 'Updated')
        self.assertEqual(updated_profile.last_name, 'Profile')

        # Simulate logging out
        self.client.logout()

        # Simulate counting notifications for an unauthenticated user
        response = self.client.get(reverse('some_other_view'))  # A view that uses CountNotifications
        self.assertEqual(response.context['count_notifications'], 0)
