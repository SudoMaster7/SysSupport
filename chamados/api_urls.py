from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .api_views import ChamadoViewSet, UnidadeViewSet, UserViewSet

router = DefaultRouter()
router.register(r'chamados', ChamadoViewSet, basename='api-chamados')
router.register(r'unidades', UnidadeViewSet, basename='api-unidades')
router.register(r'users', UserViewSet, basename='api-users')

urlpatterns = [
    path('', include(router.urls)),
]
