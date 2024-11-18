from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from .models import Question
from .api.serializers import QuestionSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class LikeTests(APITestCase):

    def test_get_like(self):
        url = reverse('like-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class AnwserTests(APITestCase):

    def test_get_answer(self):
        url = reverse('answer-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_answer(self):
        url = reverse('answer-list-create')
        data = {
            'content': 'This is a test answer.',
            'question': 1,
            'author': 1
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class QuestionTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.question = Question.objects.create(title='Test Question', content='This is a test question.', author=self.user, category='frontend')
        # self.client = APIClient()
        # self.client.login(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient() 
        self.client.credentials(HTTP_AUTHORIZATION='Token' + self.token.key)

    def test_list_post_question(self):
        url = reverse('question-list')
        data = {
            'title': 'Test Question 1',
            'content': 'This is another test question.',
            'author': self.user.id,
            'category': 'frontend'
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_detail_question(self):
        url = reverse('question-detail', kwargs={'pk': self.question.id})
        response = self.client.get(url)
        expected_data = QuestionSerializer(self.question).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)
