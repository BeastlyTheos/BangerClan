from django import forms
from django.contrib.auth.forms import UserCreationForm

from . import models


class PlayerCreationForm(UserCreationForm):
	"""
	A form that creates a player, with no privileges or chars, from the given playername and
	password. After which, a PendingCharPairing object is queued for further processing
	"""
	error_messages = {
		'password_mismatch': "The two password fields didn't match.",
	}

	initial_char = forms.CharField( max_length=16)
	class Meta:
		model = models.Player
		fields = ("email",)
