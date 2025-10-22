from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('profile/', views.ProfileDetailView.as_view(), name='profile-detail'),
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/create/', views.UserCreateView.as_view(), name='user-create'),
    path('users/<int:pk>/edit/', views.UserEditView.as_view(), name='user-edit'),
    path('users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user-delete'),
]
