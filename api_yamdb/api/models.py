from django.db import models


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
        Genre, on_delete=models.SET_NULL,
        related_name="genre", blank=True, null=True,
        through='AchievementCat',
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name="category", blank=True, null=True,
    )

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL)
    title = models.ForeignKey(Title, on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.genre} {self.title}'
