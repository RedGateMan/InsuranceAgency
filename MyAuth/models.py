from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models

# CONSTANTS
USER_TYPE = [
	("ADMIN", "Admin"),
	("CLIENT", "Client"),
	("AGENT", "Agent"),
]


# Create your models here.w


class AccountManager(BaseUserManager):
	def create_user(self, email, username, password=None, phone=None):
		if not email:
			raise ValueError("User must have an Email address")
		if not username:
			raise ValueError("User must have a Username")
		user = self.model(
			email=self.normalize_email(email),
			username=username,
			phone=phone
		)
		user.set_password(password)
		user.save(using=self.db)
		return user

	def create_superuser(self, email, username, password, phone):
		user = self.create_user(
			email=self.normalize_email(email),
			username=username,
			password=password,
			phone=phone
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self.db)
		return user


class User(AbstractBaseUser):
	name = models.CharField(max_length=15)
	surname = models.CharField(max_length=20)
	patronymic = models.CharField(max_length=20)
	username = models.CharField(max_length=30, unique=True)
	email = models.EmailField(verbose_name='email', unique=True)
	phone = models.CharField(max_length=20)
	date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)

	objects = AccountManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['phone', 'username', ]

	def __str__(self):
		return f'[#{self.id}] {self.name + " " + self.surname}'

	def has_perm(self, perm, obj=None):
		return self.is_admin

	def has_module_perms(self, app_label):
		return True
