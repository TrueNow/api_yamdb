from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField('Никнейм', max_length=150, unique=True)
    email = models.EmailField('Почта', unique=True)
    role = models.CharField('Роль', max_length=20, default='user')
    bio = models.TextField('О себе', blank=True)
    first_name = models.CharField('Имя', max_length=30, blank=True)
    last_name = models.CharField('Фамилия', max_length=150, blank=True)


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Title(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    description = models.TextField()
    genre = models.ManyToManyField(
        Genre, related_name="genre", blank=True, null=True,
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name="category", blank=True, null=True,
    )

    def __str__(self):
        return self.name
