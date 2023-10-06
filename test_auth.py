import unittest
import json
from flask import request

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from authy import PasswordChange, Signup

# Signup
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



# PasswordChange


from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import login

class PasswordChangeViewTest(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
    
    def test_password_change_view_with_valid_data(self):
        # Create a dictionary with valid form data
        valid_data = {
            'new_password': 'new_testpassword',
        }
        
        # Send a POST request to the password change view with valid data
        response = self.client.post(reverse('password_change'), data=valid_data)
        
        # Check if the response status code is 302 (redirect to change_password_done on success)
        self.assertEqual(response.status_code, 302)
        
        # Refresh the user instance from the database
        self.user.refresh_from_db()
        
        # Check if the user's password has been updated
        self.assertTrue(self.user.check_password('new_testpassword'))
    
    def test_password_change_view_with_invalid_data(self):
        # Create a dictionary with invalid form data (missing required fields)
        invalid_data = {
            'new_password': '',  # Missing new password
        }
        
        # Send a POST request to the password change view with invalid data
        response = self.client.post(reverse('password_change'), data=invalid_data)
        
        # Check if the response status code is 200 (form validation failed)
        self.assertEqual(response.status_code, 200)
        
        # Check if the form errors are displayed in the response content
        self.assertContains(response, "This field is required.")
