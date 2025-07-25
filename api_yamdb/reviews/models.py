from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from django.db import models
from django.utils import timezone

import api_yamdb.constants as constants

SLUG_VALIDATOR = RegexValidator(regex=constants.SLUG_REGEX,
                                message=constants.SLUG_ERROR)

User = get_user_model()


def validate_current_year(value):
    current_year = timezone.now().year
    if value > current_year:
        raise ValidationError(
            f'Год выпуска не может быть больше текущего ({current_year})'
        )


class Category(models.Model):
    name = models.CharField(max_length=constants.CATEGORY_NAME_MAX_LENGTH,
                            verbose_name='Название категории')
    slug = models.SlugField(
        max_length=constants.CATEGORY_SLUG_MAX_LENGTH,
        unique=True,
        verbose_name='Slug категории',
        validators=[SLUG_VALIDATOR],
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=constants.GENRE_NAME_MAX_LENGTH,
                            verbose_name='Название жанра')
    slug = models.SlugField(
        max_length=constants.GENRE_SLUG_MAX_LENGTH,
        unique=True,
        verbose_name='Slug жанра',
        validators=[SLUG_VALIDATOR],
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['name']

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=constants.TITLE_NAME_MAX_LENGTH,
        verbose_name='Название произведения',
        null=False,
    )
    year = models.IntegerField(
        verbose_name='Год выпуска',
        null=False,
        validators=[validate_current_year],
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        default='',  # Устанавливаем пустую строку по умолчанию
    )
    genre = models.ManyToManyField(
        Genre, related_name='titles', verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['name']

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор',
    )
    text = models.TextField(verbose_name='Текст отзыва')
    score = models.IntegerField(
        validators=[
            MinValueValidator(constants.REVIEW_SCORE_MIN,
                              message=('Оценка не может быть меньше '
                                       f'{constants.REVIEW_SCORE_MIN}')),
            MaxValueValidator(constants.REVIEW_SCORE_MAX,
                              message=('Оценка не может быть больше '
                                       f'{constants.REVIEW_SCORE_MAX}')),
        ],
        verbose_name='Оценка',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации'
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'], name='unique_title_author'
            )
        ]

    def __str__(self):
        return f'Отзыв от {self.author.username} на "{self.title.name}"'


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
    )
    text = models.TextField(verbose_name='Текст комментария')
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-pub_date']

    def __str__(self):
        return f'Комментарий от {self.author.username}'
