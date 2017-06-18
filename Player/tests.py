from django.test import TestCase, Client

from Player.models import Player


class Registration(TestCase):

	@classmethod
	def setUpClass(self):
		super(Registration, self).setUpClass()
		self.client = Client()
		self.email = "you@example.com"
		self.password = "aoeueoao"
		self.password2 = "ueoaoeue"
		self.initial_char = "enis"

	def test_registrationFlow(self):
		response = self.client.post(
			"/player/register/", {
				"email":self.email,
				"password1":self.password,
				"password2":self.password,
				"initial_char":self.initial_char,
			}
		)
		self.assertNotIn("<form", response.content.__str__(), "email %s and password %s does not redirect to a page without a form (IE: the confirmation page)".format(self.email, self.password))
		users = Player.objects.filter(email=self.email)
		self.assertEqual(users.count(), 1, "email %s and password %s does not create a user in the database".format(self.email, self.password))
		users.delete()
