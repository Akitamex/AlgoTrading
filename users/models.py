from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


from django.contrib.auth.models import AbstractUser, BaseUserManager ## A new class is imported. ##
from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import date

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)
        

class Role(models.Model):
    name = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return self.name


class Referal(models.Model):
    referal_code = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='referrals')
    
    def __str__(self):
        return self.referal_code


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None
    email = models.EmailField(('email address'), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    password = models.CharField(max_length=128)
    registered_at = models.DateTimeField(auto_now_add=True)
    referal = models.ForeignKey('Referal', on_delete=models.SET_NULL, null=True, default=None)
    objects = UserManager()


class Subscription(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='subscriptions')
    role = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True)
    start_date = models.DateTimeField(auto_now=True)
    end_date = models.DateTimeField(null=True, blank=True, default=None)
