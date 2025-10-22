from django.urls import path

from . import views

app_name = 'chamados'

urlpatterns = [
    path('', views.ChamadoListView.as_view(), name='lista'),
    path('novo/', views.ChamadoCreateView.as_view(), name='criar'),
    path('<int:pk>/', views.ChamadoDetailView.as_view(), name='detalhe'),
    path('<int:pk>/atualizar/', views.ChamadoAdminUpdateView.as_view(), name='atualizar'),
    path('<int:pk>/atualizar-status/', views.ChamadoTecnicoUpdateView.as_view(), name='atualizar-status'),
    path('<int:pk>/finalizar/', views.ChamadoFinalizarView.as_view(), name='finalizar'),
    path('api/tempo-espera/', views.TempoEsperaAPIView.as_view(), name='tempo-espera'),
]
