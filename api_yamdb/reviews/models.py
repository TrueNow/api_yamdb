from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField('Никнейм', max_length=150, unique=True)
    email = models.EmailField('Почта', unique=True)
    role = models.CharField('Роль', max_length=20, default='user')
    bio = models.TextField('О себе', blank=True)
    first_name = models.CharField('Имя', max_length=30, blank=True)
    last_name = models.CharField('Фамилия', max_length=150, blank=True)
