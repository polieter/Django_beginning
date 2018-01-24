from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.urls import resolve
from django.test import TestCase

from .models import Boards
from .models import Topic
from .models import Post

from .views import home
from .views import board_topics
from .views import new_topic

from .forms import NewTopicForm


class BaseTestClass(TestCase):

    def setUp(self):
        self.board = Boards.objects.create(name='Django', description='Django boards.')
        User.objects.create_user(username='john', email='john@doe.com', password='123')
        self.client.login(username='john', password='123')

    def view_status_code_test(self, url_name, status_code, **kwargs):
        url = reverse(url_name, **kwargs)
        response = self.client.get(url)
        self.assertEquals(response.status_code, status_code)

    def return_correct_viev_for_requested_url_test(self, url_, view_):
        view = resolve(url_)
        self.assertEquals(view.func, view_)


class HomeTests(BaseTestClass):

    def setUp(self):
        super().setUp()
        url = reverse('home')
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        self.view_status_code_test('home', 200)

    def test_home_url_resolves_hom_view(self):
        self.return_correct_viev_for_requested_url_test('/', home)

    def test_home_view_contains_link_to_topics_page(self):
        board_topics_url = reverse('board_topics', kwargs={'board_primary_key': self.board.pk})
        self.assertContains(self.response, 'href="{0}"'.format(board_topics_url))


class BoardsTopicsTests(BaseTestClass):

    def test_board_topics_view_sucess_ststus_code(self):
        self.view_status_code_test('board_topics', 200, kwargs={'board_primary_key': 1})

    def test_board_topics_view_not_found_status_code(self):
        self.view_status_code_test('board_topics', 404, kwargs={'board_primary_key': 99})

    def test_board_topics_url_resolves_board_topics_view(self):
        self.return_correct_viev_for_requested_url_test('/boards/1/', board_topics)

    def test_board_topics_view_contains_navigation_links(self):
        board_topics_url = reverse('board_topics', kwargs={'board_primary_key': 1})
        homepage_url = reverse('home')
        new_topic_url = reverse('new_topic', kwargs={'board_primary_key': 1})

        response = self.client.get(board_topics_url)

        self.assertContains(response, 'href="{0}"'.format(homepage_url))
        self.assertContains(response, 'href="{0}"'.format(new_topic_url))


class NewTopicTests(BaseTestClass):

    def test_new_topic_view_success_status_code(self):
        self.view_status_code_test('new_topic', 200, kwargs={'board_primary_key': 1})

    def test_new_topic_view_not_found_status_code(self):
        self.view_status_code_test('new_topic', 404, kwargs={'board_primary_key': 99})

    def test_new_topic_url_resolves_new_topic_view(self):
        self.return_correct_viev_for_requested_url_test('/boards/1/new', new_topic)

    def test_new_topic_view_contains_link_back_to_board_topics_view(self):
        new_topic_url = reverse('new_topic', kwargs={'board_primary_key': 1})
        board_topics_url = reverse('board_topics', kwargs={'board_primary_key': 1})
        response = self.client.get(new_topic_url)
        self.assertContains(response, 'href="{0}"'.format(board_topics_url))

    def test_csrf(self):
        url = reverse('new_topic', kwargs={'board_primary_key': 1})
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_new_topic_valid_post_data(self):
        url = reverse('new_topic', kwargs={'board_primary_key': 1})

        data = {
            'subject': 'Test title',
            'message': 'Lorem ipsum dolor sit amet'
        }

        response = self.client.post(url, data)
        self.assertTrue(Topic.objects.exists())
        self.assertTrue(Post.objects.exists())

    def test_new_topic_invalid_post_data(self):
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = reverse('new_topic', kwargs={'board_primary_key': 1})
        response = self.client.post(url, {})
        self.assertEquals(response.status_code, 200)

    def test_new_topic_invalid_post_data_empty_fields(self):
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = reverse('new_topic', kwargs={'board_primary_key': 1})
        data = {
            'subject': '',
            'message': ''
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Topic.objects.exists())
        self.assertFalse(Post.objects.exists())

    def test_contains_form(self):
        url = reverse('new_topic', kwargs={'board_primary_key': 1})
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, NewTopicForm)

    def test_new_topic_invalid_post_data(self):
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = reverse('new_topic', kwargs={'board_primary_key': 1})
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)