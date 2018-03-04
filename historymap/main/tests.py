from django.test import TestCase
# Create your tests here.
from historymap.main.home import home 
from django.urls import resolve
from django.template.loader import render_to_string

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        response = self.client.get('/')
        html = response.content.decode('utf8')
        self.assertTemplateUsed(response, "main/home.html")

