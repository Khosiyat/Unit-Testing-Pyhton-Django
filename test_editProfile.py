from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile, Post
from .forms import EditProfileForm
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.decorators import login_required

class EditProfileViewTest(TestCase):
    def setUp(self):
        # Create a test user and profile
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.profile = Profile.objects.create(user=self.user)
        
        # Create a test image file
        self.image_file = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")

    def test_edit_profile_view_get(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Simulate a GET request to the edit profile page
        url = reverse('edit_profile')
        response = self.client.get(url)

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

    def test_edit_profile_view_post(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Simulate a POST request to the edit profile page with valid form data
        url = reverse('edit_profile')
        form_data = {
            'first_name': 'Updated First Name',
            'last_name': 'Updated Last Name',
            'location': 'Updated Location',
            'picture': self.image_file,  # Include a test image file
        }
        response = self.client.post(url, form_data, format='multipart')

        # Check if the response status code is 302 (redirect to index on success)
        self.assertEqual(response.status_code, 302)

        # Refresh the profile instance from the database
        self.profile.refresh_from_db()

        # Check if the profile fields have been updated
        self.assertEqual(self.profile.first_name, 'Updated First Name')
        self.assertEqual(self.profile.last_name, 'Updated Last Name')
        self.assertEqual(self.profile.location, 'Updated Location')
        self.assertIsNotNone(self.profile.picture)

    def test_edit_profile_view_post_invalid_data(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Simulate a POST request to the edit profile page with invalid form data
        url = reverse('edit_profile')
        form_data = {}  # Missing required fields
        response = self.client.post(url, form_data)

        # Check if the response status code is 200 (form validation failed)
        self.assertEqual(response.status_code, 200)

        # Check if the form errors are displayed in the response content
        self.assertContains(response, "This field is required")

    def test_edit_profile_view_requires_login(self):
        # Simulate a GET request to the edit profile page without logging in
        url = reverse('edit_profile')
        response = self.client.get(url)

        # Check if the response status code is 302 (redirect to the login page)
        self.assertEqual(response.status_code, 302)

        # Check if the user is redirected to the login page
        self.assertRedirects(response, reverse('login'))

    def test_edit_profile_view_post_requires_login(self):
        # Simulate a POST request to the edit profile page without logging in
        url = reverse('edit_profile')
        form_data = {
            'first_name': 'Updated First Name',
            'last_name': 'Updated Last Name',
            'location': 'Updated Location',
            'picture': self.image_file,
        }
        response = self.client.post(url, form_data, format='multipart')

        # Check if the response status code is 302 (redirect to the login page)
        self.assertEqual(response.status_code, 302)

        # Check if the user is redirected to the login page
        self.assertRedirects(response, reverse('login'))
