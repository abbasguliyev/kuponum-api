from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action

from django_filters.rest_framework import DjangoFilterBackend

from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from account.api import serializers, filters, permissions, services, selectors

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'delete']
    queryset = selectors.user_list()
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.UserFilter

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.UserCreateSerializer
        elif self.action == 'update':
            return serializers.UserUpdateSerializer
        return super().get_serializer_class()
    
    def get_permissions(self):
        if self.action in ['create']:
            return [AllowAny()]
        if self.action in ['list']:
            return [AllowAny()]
        if self.action in ['retrieve', 'update']:
            return [permissions.IsSelfOrAdmin()]
        if self.action in ['me', 'change_password']:
            return [IsAuthenticated()]
        return super().get_permissions()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_input = services.UserCreateInput(**serializer.validated_data)
        services.create_user(user_input)
        headers = self.get_success_headers(serializer.data)
        return Response(data={"detail": _("Əməliyyat yerinə yetirildi")}, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        user_input = services.UserUpdateInput(**serializer.validated_data)
        services.update_user(instance, user_input)
        return Response(data={"detail": _("Əməliyyat yerinə yetirildi")}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def change_password(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = serializers.ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.change_password(user, **serializer.validated_data)
        return Response(data={"detail": _("Şifrə uğurla dəyişdirildi")}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request, *args, **kwargs):
        user = request.user
        serializer = serializers.UserSerializer(user)
        return Response(serializer.data)