from django.db import models
from googletrans import Translator
from googletrans.constants import LANGUAGES
from django.utils.translation import pgettext_lazy
from django.contrib.auth.models import AbstractUser, BaseUserManager
import concurrent.futures
import base64
from uuid import uuid4
import random


class UserManager(BaseUserManager):
    def create(self, password, **kwargs):
        user = self.model(
            profile=UserProfile.objects.create(),
            settings=UserSetting.objects.create(),
            **kwargs,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, password, **kwargs):
        kwargs["is_staff"] = True
        kwargs["is_superuser"] = True

        user = self.create(password, **kwargs)
        return user


class User(AbstractUser):
    objects = UserManager()

    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)

    profile = models.OneToOneField(
        'UserProfile', on_delete=models.CASCADE)
    settings = models.OneToOneField(
        'UserSetting', on_delete=models.CASCADE)


class UserProfile(models.Model):
    first_name = models.CharField(max_length=50)
    second_name = models.CharField(max_length=50)
    image = models.TextField(null=True, blank=True)


class UserSetting(models.Model):

    show_second_name = models.BooleanField(default=False)
