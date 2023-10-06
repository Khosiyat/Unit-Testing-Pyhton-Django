Import necassary files
```
import unittest
import json
from flask import request
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
```


```
class SignupViewTest(TestCase):
    def test_signup_view_with_valid_data(self):
        # Create a dictionary with valid form data
        valid_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword',
        }
        
        # Send a POST request to the signup view with valid data
        response = self.client.post(reverse('signup'), data=valid_data)
        
        # Check if the response status code is 302 (redirect to index on success)
        self.assertEqual(response.status_code, 302)
        
        # Check if a user with the provided username exists
        self.assertTrue(User.objects.filter(username='testuser').exists())
    
    def test_signup_view_with_invalid_data(self):
        # Create a dictionary with invalid form data (missing required fields)
        invalid_data = {
            'username': '',  # Missing username
            'email': 'test@example.com',
            'password': '',  # Missing password
        }
        
        # Send a POST request to the signup view with invalid data
        response = self.client.post(reverse('signup'), data=invalid_data)
        
        # Check if the response status code is 200 (form validation failed)
        self.assertEqual(response.status_code, 200)
        
        # Check if the form errors are displayed in the response content
        self.assertContains(response, "This field is required.")
```
