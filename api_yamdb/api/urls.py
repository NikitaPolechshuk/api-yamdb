from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register('users', views.UserViewSet, basename='users')
router.register('categories', views.CategoryViewSet, basename='categories')
router.register('genres', views.GenreViewSet, basename='genres')
router.register('titles', views.TitleViewSet, basename='titles')

urlpatterns = [
    path('v1/auth/signup/', views.signup, name='signup'),
    path('v1/auth/token/', views.token, name='token'),
    path('v1/', include(router.urls)),
    # Reviews endpoints
    path(
        'v1/titles/<int:title_id>/reviews/',
        views.ReviewViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='reviews-list',
    ),
    path(
        'v1/titles/<int:title_id>/reviews/<int:pk>/',
        views.ReviewViewSet.as_view(
            {'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'}
        ),
        name='reviews-detail',
    ),
    # Comments endpoints
    path(
        'v1/titles/<int:title_id>/reviews/<int:review_id>/comments/',
        views.CommentViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='comments-list',
    ),
    path(
        'v1/titles/<int:title_id>/reviews/<int:review_id>/comments/<int:pk>/',
        views.CommentViewSet.as_view(
            {'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'}
        ),
        name='comments-detail',
    ),
]
