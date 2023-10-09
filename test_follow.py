from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile, Follow, Stream
from .views import follow

class FollowViewTest(TestCase):
    def setUp(self):
        # Create two test users
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.user2 = User.objects.create_user(username='user2', password='password2')

    def test_follow_view_with_login_and_follow(self):
        # Log in user1
        self.client.login(username='user1', password='password1')

        # Simulate a GET request to follow user2
        url = reverse('follow', args=['user2', '1'])
        response = self.client.get(url)

        # Check if the response is a redirect to user2's profile
        self.assertRedirects(response, reverse('profile', args=['user2']))

        # Check if a Follow relationship exists
        self.assertTrue(Follow.objects.filter(follower=self.user1, following=self.user2).exists())

        # Check if Stream entries are created
        self.assertTrue(Stream.objects.filter(user=self.user1, post__user=self.user2).exists())

    def test_follow_view_with_login_and_unfollow(self):
        # Log in user1 and follow user2
        self.client.login(username='user1', password='password1')
        Follow.objects.create(follower=self.user1, following=self.user2)

        # Simulate a GET request to unfollow user2
        url = reverse('follow', args=['user2', '0'])
        response = self.client.get(url)

        # Check if the response is a redirect to user2's profile
        self.assertRedirects(response, reverse('profile', args=['user2']))

        # Check if the Follow relationship is deleted
        self.assertFalse(Follow.objects.filter(follower=self.user1, following=self.user2).exists())

        # Check if Stream entries are deleted
        self.assertFalse(Stream.objects.filter(user=self.user1, post__user=self.user2).exists())

    def test_follow_view_without_login(self):
        # Simulate a GET request to follow user2 without logging in
        url = reverse('follow', args=['user2', '1'])
        response = self.client.get(url)

        # Check if the response is a redirect to the login page
        self.assertRedirects(response, reverse('login'))
