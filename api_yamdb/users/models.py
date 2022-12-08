from django.contrib.auth.models import AbstractUser
from django.db import models


USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'


class User(AbstractUser):
    ROLES = (
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    )

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(
        verbose_name='Роль', max_length=20, choices=ROLES, default=USER
    )
    bio = models.TextField(verbose_name='О себе', blank=True)

    class Meta:
        ordering = ('-id',)

    @property
    def is_admin(self):
        return bool(self.role == ADMIN or self.is_staff)

    @property
    def is_moderator(self):
        return bool(self.role == MODERATOR)
