from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

import api_yamdb.constants as constants
from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150, validators=[UnicodeUsernameValidator()]
    )
    email = serializers.EmailField(max_length=254)

    class Meta:
        fields = ('username', 'email')

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                constants.USER_USERNAME_ME_ERROR
            )
        return value

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')

        if username and email:
            username_exists = User.objects.filter(username=username).exists()
            email_exists = User.objects.filter(email=email).exists()
            username_and_email_exists = username_exists and email_exists

            if username_and_email_exists:
                if not User.objects.filter(username=username,
                                           email=email
                                           ).exists():
                    raise serializers.ValidationError({
                        'username': constants.USER_USERNAME_OCCUPIED_ERROR,
                        'email': constants.USER_EMAIL_OCCUPIED_ERROR
                    })
            elif username_exists:
                raise serializers.ValidationError({
                    'username': constants.USER_USERNAME_OCCUPIED_ERROR
                })
            elif email_exists:
                raise serializers.ValidationError({
                    'email': constants.USER_EMAIL_OCCUPIED_ERROR
                })

        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'], email=validated_data['email']
        )
        return user


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        confirmation_code = attrs.get('confirmation_code')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                constants.USER_NOT_FOUND_ERROR, code='not_found'
            )

        if user.confirmation_code != confirmation_code:
            raise serializers.ValidationError(
                constants.USER_WRONG_CONFIRMATION_CODE_ERROR
            )

        attrs['user'] = user
        return attrs

    def create(self, validated_data):
        user = validated_data['user']
        refresh = RefreshToken.for_user(user)
        return {
            'token': str(refresh.access_token),
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                constants.USER_USERNAME_ME_ERROR
            )
        return value


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        read_only_fields = ('role',)

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                constants.USER_USERNAME_ME_ERROR
            )
        return value


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')
        extra_kwargs = {'name': {'required': True}, 'slug': {'required': True}}

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                constants.CATEGORY_EMPTY_NAME_ERROR
            )
        return value

    def validate_slug(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                constants.CATEGORY_EMPTY_SLUG_ERROR
            )
        return value


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.SerializerMethodField()
    description = serializers.CharField(allow_blank=True)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )
        read_only_fields = ('id', 'rating')

    def get_rating(self, obj):
        return getattr(obj, 'calculated_rating', None)


class TitleWriteSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=256,
        allow_blank=False,  # Запрещаем пустые строки
    )
    year = serializers.IntegerField(
        allow_null=False,  # Запрещаем null значения
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
        allow_empty=False,  # Запрещаем пустой список
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = ('name', 'year', 'description', 'genre', 'category')
        extra_kwargs = {
            'name': {'required': True},
            'year': {'required': True},
            'description': {'required': False},
        }

    def to_representation(self, instance):
        # Переключаемся на ReadSerializer для вывода
        return TitleReadSerializer(instance, context=self.context).data

    def validate_name(self, value):
        """Проверка что название не пустое"""
        if not value.strip():
            raise serializers.ValidationError(
                constants.TITLE_EMPTY_NAME_ERROR
            )
        return value

    def validate_genre(self, value):
        """Дополнительная валидация поля genre"""
        if not value:
            raise serializers.ValidationError(
                constants.TITLE_GENRE_REQUIRED_ERROR
            )
        return value

    def validate_year(self, value):
        if value is None:
            raise serializers.ValidationError(
                constants.TITLE_YEAR_CANNOT_BE_EMPTY_ERROR
            )
        if value > datetime.now().year:
            raise serializers.ValidationError(
                constants.TITLE_YEAR_CANNOT_BE_GT_CURRENT_ERROR
            )
        return value

    def validate(self, data):
        """Глобальная валидация для PATCH-запросов"""
        if not data:
            raise serializers.ValidationError(
                constants.TITLE_PATCH_VALIDATION_ERROR
            )
        return data


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('id', 'author', 'pub_date')

    def validate_score(self, value):
        if value < 1 or value > 10:
            raise serializers.ValidationError(
                constants.REVIEW_SCORE_VALIDATION_ERROR
            )
        return value

    def validate(self, data):
        request = self.context.get('request')
        title_id = self.context.get('view').kwargs.get('title_id')

        if request and request.method == 'POST':
            if Review.objects.filter(
                title_id=title_id, author=request.user
            ).exists():
                raise serializers.ValidationError(
                    constants.REVIEW_ALREADY_EXISTS_ERROR
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('id', 'author', 'pub_date')
