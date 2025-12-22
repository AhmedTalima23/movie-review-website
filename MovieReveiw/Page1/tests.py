from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.hashers import check_password, make_password
import json
from .models import User, Admin

class AuthTests(TestCase):
    def setUp(self):
        # Create test user
        self.test_user = User.objects.create(
            first_name='Test',
            last_name='User',
            email='testuser@example.com',
            password=make_password('testpassword'),
            role='user'
        )
        # Create test admin
        self.test_admin = Admin.objects.create(
            first_name='Test',
            last_name='Admin',
            email='testadmin@example.com',
            password=make_password('testpassword'),
            role='admin'
        )

    def test_signup_user_success(self):
        """Test successful user signup"""
        data = {
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@example.com',
            'password': 'password123',
            'confirm_password': 'password123',
            'role': 'user'
        }
        response = self.client.post(reverse('signup'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertTrue(response_data['success'])
        self.assertIn('Account created successfully', response_data['message'])
        # Check user was created
        user = User.objects.get(email='newuser@example.com')
        self.assertEqual(user.first_name, 'New')
        self.assertTrue(check_password('password123', user.password))

    def test_signup_admin_success(self):
        """Test successful admin signup"""
        data = {
            'first_name': 'New',
            'last_name': 'Admin',
            'email': 'newadmin@example.com',
            'password': 'password123',
            'confirm_password': 'password123',
            'role': 'admin'
        }
        response = self.client.post(reverse('signup'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertTrue(response_data['success'])
        # Check admin was created
        admin = Admin.objects.get(email='newadmin@example.com')
        self.assertEqual(admin.first_name, 'New')
        self.assertTrue(check_password('password123', admin.password))

    def test_signup_duplicate_email(self):
        """Test signup with existing email"""
        data = {
            'first_name': 'Another',
            'last_name': 'User',
            'email': 'testuser@example.com',  # Existing email
            'password': 'password123',
            'confirm_password': 'password123',
            'role': 'user'
        }
        response = self.client.post(reverse('signup'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertFalse(response_data['success'])
        self.assertIn('already exists', response_data['message'])

    def test_signup_password_mismatch(self):
        """Test signup with mismatched passwords"""
        data = {
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@example.com',
            'password': 'password123',
            'confirm_password': 'differentpassword',
            'role': 'user'
        }
        response = self.client.post(reverse('signup'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertFalse(response_data['success'])
        self.assertIn('Passwords do not match', response_data['message'])

    def test_login_user_success(self):
        """Test successful user login"""
        data = {
            'email': 'testuser@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(reverse('login'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertTrue(response_data['success'])
        self.assertIn('Welcome back', response_data['message'])
        # Check session
        self.assertEqual(self.client.session['user_type'], 'user')
        self.assertEqual(self.client.session['user_role'], 'user')

    def test_login_admin_success(self):
        """Test successful admin login"""
        data = {
            'email': 'testadmin@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(reverse('login'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertTrue(response_data['success'])
        self.assertEqual(self.client.session['user_type'], 'admin')
        self.assertEqual(self.client.session['user_role'], 'admin')

    def test_login_wrong_password(self):
        """Test login with wrong password"""
        data = {
            'email': 'testuser@example.com',
            'password': 'wrongpassword'
        }
        response = self.client.post(reverse('login'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertFalse(response_data['success'])
        self.assertIn('Invalid email or password', response_data['message'])

    def test_login_nonexistent_user(self):
        """Test login with non-existent email"""
        data = {
            'email': 'nonexistent@example.com',
            'password': 'password123'
        }
        response = self.client.post(reverse('login'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertFalse(response_data['success'])
        self.assertIn('Invalid email or password', response_data['message'])

    def test_signup_get_request(self):
        """Test GET request to signup renders template"""
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')

    def test_login_get_request(self):
        """Test GET request to login renders template"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
