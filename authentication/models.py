from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.db import models

class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have a valid email address.')

        if not kwargs.get('username'):
            raise ValueError('Users must have a valid username.')

        account = self.model(
            email=self.normalize_email(email), 
            username=kwargs.get('username')
        )

        account.set_password(password)
        account.save()

        return account

    def create_superuser(self, email, password, **kwargs):
        account = self.create_user(email, password, **kwargs)

        account.is_admin = True
        account.save()

        return account


class Account(AbstractBaseUser):
	
	email = models.EmailField(unique=True)

	# Used for the purpose of display, not login
	username = models.CharField(max_length=40, unique=True)

	# Can be blank if the users don't want to share their names
	first_name = models.CharField(max_length=40, blank=True)
	last_name = models.CharField(max_length=40, blank=True)

	tagline = models.CharField(max_length=40, unique=True)
	
	is_admin = models.BooleanField(default=False)

	# Auto now add is a write on creation 
	created_at = models.DateTimeField(auto_now_add=True)
	# Auto now is an upsert for the field 
	updated_at = models.DateTimeField(auto_now=True)

	object = AccountManager()

	USERNAME_FIELD = "email"

	# Must specify required fields because this class is replacing the existing model
	# If we weren't doing this then we would just need to set usernames arrtibutre
	# required = True 
	REQUIRED_FIELDS = ["username"]

	def __unicode__(self):
		return self.email

	def get_full_name(self):
		return ' '.join([self.first_name, self.last_name])

	def get_short_name(self):
		return self.first_name