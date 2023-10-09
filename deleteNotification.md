```python
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Notification
```


`class DeleteNotificationViewTest(TestCase):`
Create a test user
```python
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
```
Create a test notification for the user
```python
        self.notification = Notification.objects.create(user=self.user, message='Test notification')
```
`def test_delete_notification(self):`
Get the initial count of notifications for the user
```python

        initial_count = Notification.objects.filter(user=self.user).count()
```
Simulate a GET request to delete the notification
```python
        url = reverse('delete_notification', args=[self.notification.id])
        response = self.client.get(url)
```
Check if the response is a redirect to the index page
```python
        self.assertRedirects(response, reverse('index'))
```
 Check if the notification has been deleted
```python
        self.assertEqual(Notification.objects.filter(user=self.user).count(), initial_count - 1)
```

`def test_delete_nonexistent_notification(self):`
Get the initial count of notifications for the user
```python
        initial_count = Notification.objects.filter(user=self.user).count()
```
Simulate a GET request to delete a nonexistent notification
```python
        url = reverse('delete_notification', args=[999])  # Using a nonexistent notification ID
        response = self.client.get(url)
```
Check if the response is a redirect to the index page
```python
        self.assertRedirects(response, reverse('index'))
```

Check if the count of notifications remains the same
```python
        self.assertEqual(Notification.objects.filter(user=self.user).count(), initial_count)
```
