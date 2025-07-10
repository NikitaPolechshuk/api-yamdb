from django.contrib.auth import get_user_model
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.filters import SearchFilter

from .serializers import (
    SignUpSerializer,
    TokenSerializer,
    UserSerializer,
    UserProfileSerializer,
)
from mdb_users.permissions import IsAdmin
from mdb_users.tokens import generate_confirmation_code, send_confirmation_code

User = get_user_model()


@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data["username"]
        email = serializer.validated_data["email"]

        user = User.objects.filter(username=username, email=email).first()
        if user:
            confirmation_code = generate_confirmation_code()
            user.confirmation_code = confirmation_code
            user.save()
            send_confirmation_code(user.email, confirmation_code)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if User.objects.filter(username=username).exists():
            return Response(
                {
                    "username": [
                        "Пользователь с таким username уже существует"
                    ],
                    "email": [],
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if User.objects.filter(email=email).exists():
            return Response(
                {
                    "username": [],
                    "email": ["Пользователь с таким email уже существует"],
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def token(request):
    serializer = TokenSerializer(data=request.data)
    if serializer.is_valid():
        token_data = serializer.save()
        return Response(token_data, status=status.HTTP_200_OK)
    if "non_field_errors" in serializer.errors:
        for error in serializer.errors["non_field_errors"]:
            if hasattr(error, "code") and error.code == "not_found":
                return Response(
                    serializer.errors, status=status.HTTP_404_NOT_FOUND
                )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    filter_backends = [SearchFilter]
    search_fields = ["username"]
    lookup_field = "username"
    http_method_names = ["get", "post", "patch", "delete"]

    @action(
        detail=False,
        methods=["get", "patch"],
        permission_classes=[permissions.IsAuthenticated],
        url_path="me",
    )
    def me(self, request):
        if request.method == "GET":
            serializer = UserProfileSerializer(request.user)
            return Response(serializer.data)
        elif request.method == "PATCH":
            serializer = UserProfileSerializer(
                request.user, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
