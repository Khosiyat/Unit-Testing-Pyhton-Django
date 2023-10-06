Import necassary files
```python
import unittest
import json
from flask import request
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
```


```python
class SignupViewTest(TestCase):
    def test_signup_view_with_valid_data(self):
```

Create a dictionary with valid form data
```python
        valid_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword',
        }
```

Send a POST request to the signup view with valid data
```python
        response = self.client.post(reverse('signup'), data=valid_data)
```

Check if the response status code is 302 (redirect to index on success)
```python
        self.assertEqual(response.status_code, 302)
```

Check if a user with the provided username exists
```python
        self.assertTrue(User.objects.filter(username='testuser').exists())
```

```python
    def test_signup_view_with_invalid_data(self):
```

Create a dictionary with invalid form data (missing required fields)
```python
        invalid_data = {
            'username': '',  # Missing username
            'email': 'test@example.com',
            'password': '',  # Missing password
        }
```

Send a POST request to the signup view with invalid data
```python
        response = self.client.post(reverse('signup'), data=invalid_data)
```

Check if the response status code is 200 (form validation failed)
```python
        self.assertEqual(response.status_code, 200)
```

Check if the form errors are displayed in the response content
```python
        self.assertContains(response, "This field is required.")
```
