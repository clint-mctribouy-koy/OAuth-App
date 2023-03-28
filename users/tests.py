from django.test import Client
from django.contrib.auth import get_user_model
from django.urls import reverse



from http import HTTPStatus

from django.test import TestCase

from .forms import RegisterForm

from .models import Profile


class ProfileViewTests(TestCase):   

    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testuser1@example.com",password="testpass123",)
    
    def test_200_unathenticated_user_when_on_homepage_has_login_option(self):
        c = Client()

        response = c.get("http://127.0.0.1:8000")

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "<h1>OAuth Application</h1>", html=True)
        self.assertContains(response, "<span>Login with GitHub</span>", html=True)


    def test_login_page_and_302_code_redirected_to_welcome_text_on_homepage(self):
        c = Client()
        c.login(username="testuser1@example.com", password="testpass123")
        response = c.post('/login/', {'username': "testuser1@example.com", 'password': "testpass123"})

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, '/')

        response = c.get('/login/', follow=True)



        self.assertContains(response, "<h3>Welcome testuser1@example.com !!!</h3>", html=True)
    
    def test_post_request_creation_of_new_profile(self):
        c = Client()
        c.login(username="testuser1@example.com", password="testpass123")
        response = c.post('/login/', {'username': "testuser1@example.com", 'password': "testpass123"})

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, '/')

        response = c.get('/login/', follow=True)

        self.assertFalse(Profile.objects.filter(first_name='Test').exists())


        response = c.post("http://localhost:8000/register/", {"first_name": "Test", "last_name": "User", "bio": "This is a bio", "past_address": "123 Real Avenue, RE3 5EW", "current_address": "321 Fake Park, FR3 7HJ"})

         
        self.assertTrue(Profile.objects.filter(first_name='Test').exists())


class ProfileFormTests(TestCase):   
    def test_first_name_starting_lowercase(self):
        form = RegisterForm(data={"first_name": "a lowercase title"})

        self.assertEqual(
            form.errors["first_name"], ["Should start with an uppercase letter"]
        )

    def test_last_name_starting_lowercase(self):
        form = RegisterForm(data={"last_name": "a lowercase title"})

        self.assertEqual(
            form.errors["last_name"], ["Should start with an uppercase letter"]
        )


 
 








