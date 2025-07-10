from datetime import datetime
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from mdb_users.tokens import generate_confirmation_code, send_confirmation_code
from reviews.models import Category, Genre, Title
import re

User = get_user_model()


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150, validators=[UnicodeUsernameValidator()]
    )
    email = serializers.EmailField(max_length=254)

    class Meta:
        fields = ("username", "email")

    def validate_username(self, value):
        if value.lower() == "me":
            raise serializers.ValidationError(
                "Имя пользователя 'me' недопустимо."
            )

        if not re.match(r"^[\w.@+-]+\Z", value):
            raise serializers.ValidationError(
                "Имя пользователя содержит недопустимые символы."
            )
        return value

    def create(self, validated_data):
        confirmation_code = generate_confirmation_code()
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            confirmation_code=confirmation_code,
        )
        send_confirmation_code(user.email, confirmation_code)
        return user


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get("username")
        confirmation_code = attrs.get("confirmation_code")

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "Пользователь с таким именем не найден.", code="not_found"
            )

        if user.confirmation_code != confirmation_code:
            raise serializers.ValidationError("Неверный код подтверждения.")

        attrs["user"] = user
        return attrs

    def create(self, validated_data):
        user = validated_data["user"]
        refresh = RefreshToken.for_user(user)
        return {
            "token": str(refresh.access_token),
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )

    def validate_username(self, value):
        if value.lower() == "me":
            raise serializers.ValidationError(
                "Имя пользователя 'me' недопустимо."
            )
        return value


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )
        read_only_fields = ("role",)

    def validate_username(self, value):
        if value.lower() == "me":
            raise serializers.ValidationError(
                "Имя пользователя 'me' недопустимо."
            )
        return value


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')
        extra_kwargs = {
            'name': {'required': True},
            'slug': {'required': True}
        }

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Название категории не может быть пустым")
        return value

    def validate_slug(self, value):
        if not value.strip():
            raise serializers.ValidationError("Slug категории не может быть пустым")
        return value


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True) 
    rating = serializers.IntegerField(read_only=True)
    description = serializers.CharField(allow_blank=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating',
            'description', 'genre', 'category'
        )
        read_only_fields = ('id', 'rating')


class TitleWriteSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=256,
        allow_blank=False,  # Запрещаем пустые строки
        required=True
    )
    year = serializers.IntegerField(
        required=True,
        allow_null=False  # Запрещаем null значения
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
        allow_empty=False  # Запрещаем пустой список
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = (
            'name', 'year', 'description',
            'genre', 'category'
        )
        extra_kwargs = {
            'name': {'required': False},
            'year': {'required': False},
            'description': {'required': False}
        }

    def to_representation(self, instance):
        # Переключаемся на ReadSerializer для вывода
        return TitleReadSerializer(instance, context=self.context).data

    def validate_name(self, value):
        """Проверка что название не пустое"""
        if not value.strip():
            raise serializers.ValidationError(
                "Название произведения не может быть пустым"
            )
        return value

    def validate_genre(self, value):
        """Дополнительная валидация поля genre"""
        if not value:
            raise serializers.ValidationError(
                "Произведение должно принадлежать хотя бы к одному жанру"
            )
        return value

    def validate_year(self, value):
        if value is None:
            raise serializers.ValidationError(
                "Год выпуска обязателен"
            )
        if value > datetime.now().year:
            raise serializers.ValidationError(
                "Год выпуска не может быть больше текущего"
            )
        return value

    def validate(self, data):
        """Глобальная валидация для PATCH-запросов"""
        if not data:
            raise serializers.ValidationError("Не указаны данные для обновления")
        return data
