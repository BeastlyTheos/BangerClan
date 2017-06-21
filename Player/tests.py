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


class ValidateAccess(TestCase):

	@classmethod
	def setUpClass(self):
		super(ValidateAccess, self).setUpClass()
		self.client = Client()
		self.user_password = "hello worlds"
		self.user = Player.objects.create_user( email="me@example.ca", password=self.user_password)
		self.char = Char(owner=self.user, name="snakr")
		self.user.current_char =  		self.char
		self.char.save()
		self.user.save()

	@classmethod
	def tearDownClass(self):
		super(ValidateAccess, self).tearDownClass()
		self.char.delete()
		self.user.delete()

	def test_loginAndLogoutFlow(self):
		response = self.client.post("/player/login", {"username":self.char.name, "password":self.user_password})
		self.assertEqual(response.status_code, 302, "logging in does not redirect")
		self.assertIn("_auth_user_id", self.client.session, "logging in does not create a session id")
		response = self.client.get("/player/logout")
		self.assertNotIn("_auth_user_id", self.client.session, "logging in does not create a session id")

	def test_profileAccess(self):
		response = self.client.get("/player/profile")
		self.assertEqual(response.status_code, 302, "accessing profile without authorisation does not redirect")
		self.assertTrue(self.client.login(username=self.char.name, password=self.user_password), "cannot log in")
		#response = self.client.get("/player/profile")
		self.assertEqual(response.status_code, 302, "authorised user cannot access profile")
		self.client.logout()
		response = self.client.get("/player/profile")
		self.assertEqual(response.status_code, 302, "accessing profile after logging out does not redirect")
