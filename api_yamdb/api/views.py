from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api_yamdb.exceptions import SendConfirmationCodeError
from mdb_users.permissions import (IsAdmin, IsAdminOrReadOnly,
                                   IsAuthorOrModeratorOrAdmin)
from mdb_users.tokens import generate_confirmation_code, send_confirmation_code
from reviews.models import Category, Genre, Review, Title

from .filters import TitleFilter
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, SignUpSerializer,
                          TitleReadSerializer, TitleWriteSerializer,
                          TokenSerializer, UserProfileSerializer,
                          UserSerializer)

User = get_user_model()


def handle_existing_user(user, email):
    confirmation_code = generate_confirmation_code()
    user.confirmation_code = confirmation_code
    user.save()
    try:
        send_confirmation_code(email, confirmation_code)
    except SendConfirmationCodeError as e:
        return Response(
            {'detail': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return Response(
        {'username': user.username, 'email': user.email},
        status=status.HTTP_200_OK,
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        email = serializer.validated_data['email']

        user = User.objects.filter(username=username, email=email).first()
        if user:
            return handle_existing_user(user, email)

        user = serializer.save()
        confirmation_code = generate_confirmation_code()
        user.confirmation_code = confirmation_code
        user.save()
        send_confirmation_code(user.email, confirmation_code)
        return Response(
            {'username': user.username, 'email': user.email},
            status=status.HTTP_200_OK,
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    serializer = TokenSerializer(data=request.data)
    if serializer.is_valid():
        token_data = serializer.save()
        return Response(token_data, status=status.HTTP_200_OK)
    if 'non_field_errors' in serializer.errors:
        for error in serializer.errors['non_field_errors']:
            if hasattr(error, 'code') and error.code == 'not_found':
                return Response(
                    serializer.errors, status=status.HTTP_404_NOT_FOUND
                )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    filter_backends = [SearchFilter]
    search_fields = ['username']
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[permissions.IsAuthenticated],
        url_path='me',
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = UserProfileSerializer(request.user)
            return Response(serializer.data)
        elif request.method == 'PATCH':
            serializer = UserProfileSerializer(
                request.user, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


class CategoryViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action == 'list':
            return []
        return super().get_permissions()


class GenreViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action == 'list':
            return []
        return super().get_permissions()


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        # Для операций чтения используем ReadSerializer
        if self.request.method == 'GET':
            return TitleReadSerializer
        # Для операций записи используем WriteSerializer
        return TitleWriteSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [AllowAny()]
        return super().get_permissions()

    def get_queryset(self):
        return Title.objects.annotate(
            calculated_rating=Avg('reviews__score')
        ).all().order_by('name')


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy'):
            return [IsAuthorOrModeratorOrAdmin()]
        return super().get_permissions()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id'),
        )
        return review.comments.all()

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy'):
            return [IsAuthorOrModeratorOrAdmin()]
        return super().get_permissions()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id'),
        )
        serializer.save(author=self.request.user, review=review)
