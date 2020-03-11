from django.test import TestCase
from django.urls import reverse
from django.urls import resolve

from boards.views import home, board_topics
from boards.models import Board
from myproject.boards.forms import NewTopicForm

# Create your tests here.
class HomeTests(TestCase):
    def setUp(self):
        Board.objects.create(name='django', description='django-board')
        url = reverse('home')
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_home_url_resolve_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home)

    def test_home_url_contains_url_link(self):
        board_topics_url= resolve('board_topics', kwargs={'pk': self.boards.pk})
        homepage_url = reverse('home')
        response = self.client.get(board_topics_url)
        self.assertContains(response, 'href="{0}"'.format(homepage_url))


class BoardTopicTests(TestCase):
    def setUp(self):
        Board.objects.create(name='django', description='django-board')

    def test_board_topic_view_status_code(self):
        url = reverse('board_topics', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_board_topic_view_url_resolve(self):
        view = resolve('/boards/1/')
        self.assertEquals(view.func, board_topics)

    def test_board_topic_view_not_found(self):
        url = reverse('board_topics', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_board_topic_reverse_link(self):
        board_topics_url = reverse('board_topics', kwargs={'pk': 1})
        response = self.client.get(board_topics_url)
        homepage_url = reverse('home')
        self.assertContains(response, 'href="{0}"'.format(homepage_url))


class NewTopicTests(TestCase):
    def setUp(self):
        Board.objects.create(name='django', description='django description')

    def test_new_topic_view_success_status(self):
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_new_topic_view_fail_status(self):
        url = reverse('new_topic', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_new_topic_url_resolve(self):
        view = resolve('/board/1/new/')
        self.assertEquals(view.func, 'new_topic')

    def test_new_topic_reverse_link(self):
        new_topic_url = reverse('new_topic', kwargs={'pk': 1})
        board_topic_url = reverse('board_topics', kwargs={'pk': 1})
        response = self.client.get(new_topic_url)
        self.assertContains(response, "href='{}'".format(board_topic_url))

    def test_new_topic_valid_form(self):
        topic_url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.get(topic_url)
        form = response.context.get('form')
        self.assertIsInstance(form, NewTopicForm)

    def test_new_topic_invalid_form(self):
        topic_url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.get(topic_url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)