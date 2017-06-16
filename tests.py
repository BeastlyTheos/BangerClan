from django.test import TestCase, Client
from django.template import loader
from django.urls import resolve


#base templates
templates = [
]


class TestTemplates(TestCase):
	def test_compile(self):
		for template_name in templates:
			template = loader.get_template(template_name)
			template.render()
