from django.core.urlresolvers import reverse
from django.urls import resolve
from django.test import TestCase
from .views import home


class HomeTests(TestCase):

    def test_home_view_status_code(self):
        '''Test if view return corrected status code 200'''
        url = reverse('home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_home_url_resolves_hom_view(self):
        '''Check if django return corrected view for the requested url'''
        view = resolve('/')
        self.assertEquals(view.func, home)
