from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    text = models.TextField(verbose_name='Отзыв')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews')
    scope = models.PositiveSmallIntegerField(
        verbose_name = 'Оценка',
        default=5,
        validators=[
            MinValueValidator(1, message='Минимальная оценка 1'),
            MaxValueValidator(10, message='Максимальная оценка 10'),
        ],
        blank=False,
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["title", "author"], name="unique_review"
            ),
        ]

    def __str__(self):
        return f'Отзыв от {self.author} на {self.title}'
