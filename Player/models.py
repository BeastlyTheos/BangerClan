from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
	use_in_migrations = True

	def _create_user(self, email, password, **extra_fields):
		"""
		Creates and saves a User with the given username, email and password.
		"""
		if not email:
			raise ValueError("The given email must be set")
		email = self.normalize_email(email)
		user = self.model(email=email, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, email=None, password=None, **extra_fields):
		extra_fields.setdefault("is_staff", False)
		extra_fields.setdefault("is_superuser", False)
		return self._create_user(email, password, **extra_fields)

	def create_superuser(self, email, password, **extra_fields):
		extra_fields.setdefault("is_staff", True)
		extra_fields.setdefault("is_superuser", True)

		if extra_fields.get("is_staff") is not True:
			raise ValueError("Superuser must have is_staff=True.")
		if extra_fields.get("is_superuser") is not True:
			raise ValueError("Superuser must have is_superuser=True.")

		return self._create_user(email, password, **extra_fields)


# A few helper functions for common logic between User and AnonymousUser.
def _user_get_all_permissions(user, obj):
	permissions = set()
	for backend in auth.get_backends():
		if hasattr(backend, "get_all_permissions"):
			permissions.update(backend.get_all_permissions(user, obj))
	return permissions

def _user_has_perm(user, perm, obj):
	"""
	A backend can raise `PermissionDenied` to short-circuit permission checking.
	"""
	for backend in auth.get_backends():
		if not hasattr(backend, "has_perm"):
			continue
		try:
			if backend.has_perm(user, perm, obj):
				return True
		except PermissionDenied:
			return False
	return False


def _user_has_module_perms(user, app_label):
	"""
	A backend can raise `PermissionDenied` to short-circuit permission checking.
	"""
	for backend in auth.get_backends():
		if not hasattr(backend, "has_module_perms"):
			continue
		try:
			if backend.has_module_perms(user, app_label):
				return True
		except PermissionDenied:
			return False
	return False


class Player(AbstractBaseUser, PermissionsMixin):
	"""
	An abstract base class implementing a fully featured User model with
	admin-compliant permissions.

	Username and password are required. Other fields are optional.
	"""

	email = models.EmailField("email address", unique=True, blank=True)
	is_staff = models.BooleanField(
		"staff status",
		default=False,
		help_text="Designates whether the user can log into this admin site.",
	)
	is_active = models.BooleanField(
		"active",
		default=True,
		help_text=
			"Designates whether this user should be treated as active. "
			"Unselect this instead of deleting accounts."
	)
	date_joined = models.DateTimeField("date joined", default=timezone.now)
	current_char = models.ForeignKey(
		"Char",
		null=True,
		help_text = 
			"This is the char name that displays when the player comments on a log"
	);

	objects = UserManager()

	USERNAME_FIELD = "email"
	REQUIRED_FIELDS = []

	class Meta:
		verbose_name = "player"
		verbose_name_plural = "players"

	def email_user(self, subject, message, from_email=None, **kwargs):
		"""
		Sends an email to this User.
		"""
		send_mail(subject, message, from_email, [self.email], **kwargs)



class Char(models.Model):
	owner = models.ForeignKey( "Player", on_delete=models.CASCADE, editable=False)
	name = models.CharField( max_length=16, unique=True)
	is_incog = models.BooleanField( default=True)
