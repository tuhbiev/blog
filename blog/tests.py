from django.http import response
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Post

class Blog(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username = 'testuser',
            email = 'test@email.com',
            password = 'secret'
        )

        self.post = Post.objects.create(
            title = 'A good title',
            body = 'Nice body content',
            author = self.user,
        )

    def test_strings_representation(self):
        post = Post(title = 'A simple title')
        self.assertEqual(str(post), post.title)

    def test_post_content(self):
        self.assertEqual(f'{self.post.title}', 'A good title')
        self.assertEqual(f'{self.post.author}', 'testuser')
        self.assertEqual(f'{self.post.body}', 'Nice body content')

    def test_post_list_wiew(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nice body content')
        self.assertTemplateUsed(response, 'home.html')

    def test_post_detail_view(self):
        response = self.client.get('/post/1/')
        no_responce = self.client.get('/post/100000')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_responce.status_code, 301)
        self.assertContains(response, 'A good title')
        self.assertTemplateUsed(response, 'post_detail.html')