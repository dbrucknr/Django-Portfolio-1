from django.contrib.auth.models import BaseUserManager, Group, GroupManager
from django.db import models, transaction
from django.contrib.auth import get_user_model
class UserManager(BaseUserManager):

    def create_user(self, email, username, groups, user_permissions, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")
        group = Group.objects.get_or_create(name='Standard')       
        user = self.model(
            email = self.normalize_email(email),
            username = username,
        )
        user.set_password(password)
        user.save(using=self._db)
        
        user_saved = get_user_model().objects.get(username=username)
        new_group = Group.objects.get(name='Standard')
        user_saved.groups.add(new_group)
        return user

    def create_superuser(self, email, username, password):

        user = self.create_user(
            email = self.normalize_email(email),
            password = password,
            username = username
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user