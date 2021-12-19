from rest_framework.test import APITestCase
from django.urls import reverse


class TestSetup(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')

        self.user_data = {
            "username": "testusername",
            "email": "test@gmail.com",
            "password": "testpassword",
            "password2": "testpassword"
        }
        self.login_data = {
            "username": "test@gmail.com",
            "password": "testpassword"
        }
        return super().setUp()
    
    def tearDown(self):
        return super().tearDown()