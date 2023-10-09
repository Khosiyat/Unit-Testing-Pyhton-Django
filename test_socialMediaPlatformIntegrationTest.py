from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Follow, Notification

class SocialMediaPlatformIntegrationTest(TestCase):
    def setUp(self):
        # Create test users
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.user2 = User.objects.create_user(username='user2', password='password2')

    def test_social_media_platform_flow(self):
        # Log in user1 and follow user2
        self.client.login(username='user1', password='password1')
        response = self.client.get(reverse('follow', args=['user2', 1]))

        # Check if the response is a redirect to user2's profile
        self.assertRedirects(response, reverse('profile', args=['user2']))

        # Check if user1 is following user2
        self.assertTrue(Follow.objects.filter(follower=self.user1, following=self.user2).exists())

        # Log in user2 and check if user1's follow resulted in a notification
        self.client.login(username='user2', password='password2')
        response = self.client.get(reverse('profile', args=['user2']))

        # Check if the response contains a notification
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'New follower: user1')

        # Log out user2 and unfollow user1
        self.client.logout()
        response = self.client.get(reverse('follow', args=['user1', 0]))

        # Check if the response is a redirect to user1's profile
        self.assertRedirects(response, reverse('profile', args=['user1']))

        # Check if user2 is not following user1 anymore
        self.assertFalse(Follow.objects.filter(follower=self.user2, following=self.user1).exists())

        # Log in user1 and verify that the notification is marked as seen
        self.client.login(username='user1', password='password1')
        response = self.client.get(reverse('view_notifications'))

        # Check if the response contains the seen notification
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'New follower: user1')

        # Check if the count of unread notifications is 0 for user1
        response = self.client.get(reverse('some_other_view'))  # A view that uses CountNotifications
        self.assertEqual(response.context['count_notifications'], 0)
