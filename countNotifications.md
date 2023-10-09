from django.test import TestCase
from django.contrib.auth.models import User
from .models import Notification
from .context_processors import CountNotifications

class CountNotificationsTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_count_notifications_authenticated_user(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Create some test notifications for the user
        Notification.objects.create(user=self.user, message='Test notification 1', is_seen=False)
        Notification.objects.create(user=self.user, message='Test notification 2', is_seen=True)

        # Call the CountNotifications function with a request context
        request = self.client.request().wsgi_request
        context = CountNotifications(request)

        # Check if the count_notifications context variable is correctly set
        self.assertEqual(context['count_notifications'], 1)  # One unread notification

    def test_count_notifications_unauthenticated_user(self):
        # Log out the user (unauthenticated)
        self.client.logout()

        # Call the CountNotifications function with a request context
        request = self.client.request().wsgi_request
        context = CountNotifications(request)

        # Check if the count_notifications context variable is 0 for unauthenticated users
        self.assertEqual(context['count_notifications'], 0)  # No notifications for unauthenticated users
