from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
	"""Manager that uses email as the unique identifier."""

	use_in_migrations = True

	def _create_user(self, email, password, **extra_fields):
		if not email:
			raise ValueError("An email address is required")
		email = self.normalize_email(email)
		user = self.model(email=email, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, email, password=None, **extra_fields):
		extra_fields.setdefault("is_staff", False)
		extra_fields.setdefault("is_superuser", False)
		return self._create_user(email, password, **extra_fields)

	def create_superuser(self, email, password=None, **extra_fields):
		extra_fields.setdefault("is_staff", True)
		extra_fields.setdefault("is_superuser", True)

		if extra_fields.get("is_staff") is not True:
			raise ValueError("Superuser must have is_staff=True")
		if extra_fields.get("is_superuser") is not True:
			raise ValueError("Superuser must have is_superuser=True")

		return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
	"""User model that authenticates with email instead of username."""

	username = None
	email = models.EmailField(_('email address'), unique=True)
	full_name = models.CharField(max_length=255, blank=True)
	is_email_verified = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)

	USERNAME_FIELD = "email"
	REQUIRED_FIELDS: list[str] = []

	objects = CustomUserManager()

	class Meta:
		ordering = ["-created_at"]

	def __str__(self) -> str:  # pragma: no cover - trivial
		return self.email
