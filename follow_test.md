```python
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile, Follow, Stream
from .views import follow
```

`class FollowViewTest(TestCase):`
Create two test users
```python
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.user2 = User.objects.create_user(username='user2', password='password2')
```

Log in user1
```python
    def test_follow_view_with_login_and_follow(self):
        self.client.login(username='user1', password='password1')
```
Simulate a GET request to follow user2
```python
        url = reverse('follow', args=['user2', '1'])
        response = self.client.get(url)
```
Check if the response is a redirect to user2's profile
```python
        self.assertRedirects(response, reverse('profile', args=['user2']))
```
Check if a Follow relationship exists
```python
        self.assertTrue(Follow.objects.filter(follower=self.user1, following=self.user2).exists())
```
Check if Stream entries are created
```python
        self.assertTrue(Stream.objects.filter(user=self.user1, post__user=self.user2).exists())
```
Log in user1 and follow user2
```python
    def test_follow_view_with_login_and_unfollow(self):
        self.client.login(username='user1', password='password1')
        Follow.objects.create(follower=self.user1, following=self.user2)
```
Simulate a GET request to unfollow user2
```python
        url = reverse('follow', args=['user2', '0'])
        response = self.client.get(url)
```
Check if the response is a redirect to user2's profile
```python
        self.assertRedirects(response, reverse('profile', args=['user2']))
```
Check if the Follow relationship is deleted
```python
        self.assertFalse(Follow.objects.filter(follower=self.user1, following=self.user2).exists())
```
Check if Stream entries are deleted
```python
        self.assertFalse(Stream.objects.filter(user=self.user1, post__user=self.user2).exists())
```

Simulate a GET request to follow user2 without logging in
```python
    def test_follow_view_without_login(self):
        url = reverse('follow', args=['user2', '1'])
        response = self.client.get(url)
```
Check if the response is a redirect to the login page
```python
        self.assertRedirects(response, reverse('login'))
```
