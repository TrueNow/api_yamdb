from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    role = models.CharField('Роль', max_length=20, default='user')
    bio = models.TextField('О себе', blank=True)

