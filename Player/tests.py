from django.test import TestCase, Client

from Player.models import Player, Char, PendingCharRegistration


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
		user = users[0]
		pending_chars = PendingCharRegistration.objects.filter(player=user, name=self.initial_char)
		self.assertEqual(pending_chars.count(), 1, "failed to create initial char named "+self.initial_char)
		pending_char = pending_chars[0]
		response = self.client.get("/player/register_char?token="+pending_char.token)
		self.assertEqual(response.status_code, 200)
		self.assertIn("successfully", response.content.__str__(), "initial char registration does not return a success page")
		self.assertFalse(PendingCharRegistration.objects.filter(pk=pending_char.pk).exists(), "Initial char registration does not delete the pending char")
		chars = Char.objects.filter(name=pending_char.name)
		self.assertEqual( chars.count(), 1, "Initial char registration does not create a char object")
		char = chars[0]
		user.refresh_from_db()
		self.assertEqual(user.current_char, char, "Initial char registration does not set current char")
		chars.delete()
		users.delete()
