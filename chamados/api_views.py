from django.contrib.auth import get_user_model
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from accounts.mixins import ADMIN_TI_GROUP, GESTOR_GROUP, TECNICO_GROUP

from .models import Chamado, Unidade
from .serializers import (
    ChamadoFinalizarSerializer,
    ChamadoSerializer,
    ChamadoUpdateSerializer,
    UnidadeSerializer,
    UserCreateSerializer,
    UserSerializer,
)

User = get_user_model()


class IsAdminTi(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and (
            user.is_superuser
            or user.is_staff
            or user.groups.filter(name=ADMIN_TI_GROUP).exists()
        )


class IsGestor(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.groups.filter(name=GESTOR_GROUP).exists()


class IsSolicitante(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.solicitante == request.user


class ChamadoViewSet(viewsets.ModelViewSet):
    queryset = Chamado.objects.select_related('unidade', 'solicitante').prefetch_related('tecnicos_designados')
    serializer_class = ChamadoSerializer

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.is_superuser or user.is_staff or user.groups.filter(name=ADMIN_TI_GROUP).exists():
            return qs
        if user.groups.filter(name=TECNICO_GROUP).exists():
            return qs.filter(tecnicos_designados=user)
        return qs.filter(solicitante=user)

    def get_permissions(self):
        if self.action in {'update', 'partial_update', 'destroy', 'atualizar'}:
            permission_classes = [IsAdminTi]
        elif self.action == 'create':
            permission_classes = [IsGestor]
        elif self.action in {'finalizar'}:
            permission_classes = [IsGestor, IsSolicitante]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True, methods=['patch'], url_path='atualizar', permission_classes=[IsAdminTi])
    def atualizar(self, request, pk=None):
        chamado = self.get_object()
        serializer = ChamadoUpdateSerializer(chamado, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(ChamadoSerializer(chamado, context={'request': request}).data)

    @action(detail=True, methods=['post'], url_path='finalizar', permission_classes=[IsGestor, IsSolicitante])
    def finalizar(self, request, pk=None):
        chamado = self.get_object()
        if chamado.status != Chamado.Status.RESOLVIDA:
            return Response({'detail': 'Chamado precisa estar com status Resolvida para ser finalizado.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ChamadoFinalizarSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(chamado)
        return Response(ChamadoSerializer(chamado, context={'request': request}).data)


class UnidadeViewSet(viewsets.ModelViewSet):
    queryset = Unidade.objects.all()
    serializer_class = UnidadeSerializer
    permission_classes = [IsAdminTi]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().select_related('profile')
    serializer_class = UserSerializer
    permission_classes = [IsAdminTi]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return super().get_serializer_class()