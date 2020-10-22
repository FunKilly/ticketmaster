from django.contrib.auth.models import BaseUserManager
from django.db import models

from .errors import MISSING_EMAIL_ERROR, MISSING_USER_NAME_ERROR


class UserManagerBase(BaseUserManager):
    def create_user(self, email, name, password):
        if not email:
            raise ValueError(MISSING_EMAIL_ERROR)
        if not name:
            raise ValueError(MISSING_USER_NAME_ERROR)

        email = email.lower()
        user = self.model(email=self.normalize_email(email), name=name,)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(email, password=password, name=name,)

        user.is_active = True
        user.is_verified = True
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save()
        return user


class UserQuerySet(models.QuerySet):
    pass


class UserManager(UserManagerBase.from_queryset(UserQuerySet)):
    use_in_migrations = True
