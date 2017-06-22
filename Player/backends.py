from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend as BaseModelBackend
from django.contrib.auth.models import Permission

from .models import Player, Char


class ModelBackend(BaseModelBackend):
	"""
	Authenticates against settings.AUTH_USER_MODEL.
	Uses a char name in place of username.
	"""

	def authenticate(self, username=None, password=None, **kwargs):
		UserModel = get_user_model()
		try:
			user = Char.objects.get(name=username).owner
		except UserModel.DoesNotExist:
			# Run the default password hasher once to reduce the timing
			# difference between an existing and a non-existing user (#20760).
			UserModel().set_password(password)
		else:
			if user.check_password(password) and self.user_can_authenticate(user):
				return user
