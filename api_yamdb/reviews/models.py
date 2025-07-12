from django.db import models
from django.core.validators import MaxValueValidator, RegexValidator
from datetime import datetime

SLUG_REGEX = '^[-a-zA-Z0-9_]+$'
SLUG_ERROR = 'Slug может содержать только буквы, цифры, дефисы и подчеркивания'
SLUG_VALIDATOR = RegexValidator(regex=SLUG_REGEX, message=SLUG_ERROR)


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название категории'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Slug категории',
        validators=[SLUG_VALIDATOR]
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название жанра'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Slug жанра',
        validators=[SLUG_VALIDATOR]
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['name']

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название произведения',
        blank=False,  # Запрещаем пустые значения
        null=False,
    )
    year = models.IntegerField(
        verbose_name='Год выпуска',
        blank=False,  # Запрещаем пустые значения
        null=False,
        validators=[
            MaxValueValidator(
                datetime.now().year,
                message='Год не может быть больше текущего'
            )
        ]
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        default=''  # Устанавливаем пустую строку по умолчанию
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория',
        null=True,
        blank=True
    )
    rating = models.IntegerField(
        verbose_name='Рейтинг',
        null=True,
        blank=True,
        editable=False
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['name']

    def __str__(self):
        return self.name
