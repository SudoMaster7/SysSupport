from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView, FormView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.shortcuts import get_object_or_404

from .forms import UserCreateForm, UserEditForm
from .mixins import AdminTIRequiredMixin
from .models import Profile

User = get_user_model()


class ProfileDetailView(LoginRequiredMixin, TemplateView):
	template_name = 'accounts/profile_detail.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['profile'] = getattr(self.request.user, 'profile', None)
		return context


class UserCreateView(AdminTIRequiredMixin, FormView):
	"""View for creating new users (Gestores and Tecnicos)."""
	form_class = UserCreateForm
	template_name = 'accounts/user_create_form.html'
	success_url = reverse_lazy('accounts:user-create')

	def form_valid(self, form):
		user = form.save()
		messages.success(self.request, f"Usuário '{user.username}' criado com sucesso!")
		return HttpResponseRedirect(self.get_success_url())

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['page_title'] = 'Criar Novo Usuário'
		return context


class UserListView(AdminTIRequiredMixin, ListView):
	"""View for listing all users (for Admin TI)."""
	model = User
	template_name = 'accounts/user_list.html'
	context_object_name = 'users'
	paginate_by = 20

	def get_queryset(self):
		queryset = User.objects.select_related('profile', 'profile__unidade').prefetch_related('groups').order_by('-date_joined')
		
		# Filter by search query
		search = self.request.GET.get('search', '')
		if search:
			queryset = queryset.filter(
				Q(username__icontains=search) |
				Q(first_name__icontains=search) |
				Q(last_name__icontains=search) |
				Q(email__icontains=search) |
				Q(profile__matricula__icontains=search)
			)
		
		# Filter by group
		group = self.request.GET.get('group', '')
		if group:
			queryset = queryset.filter(groups__name=group)
		
		return queryset

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['search'] = self.request.GET.get('search', '')
		context['selected_group'] = self.request.GET.get('group', '')
		return context


class UserEditView(AdminTIRequiredMixin, FormView):
	"""View for editing existing users."""
	form_class = UserEditForm
	template_name = 'accounts/user_edit_form.html'

	def dispatch(self, request, *args, **kwargs):
		self.user_to_edit = get_object_or_404(User, pk=kwargs.get('pk'))
		return super().dispatch(request, *args, **kwargs)

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs['user'] = self.user_to_edit
		return kwargs

	def get_initial(self):
		initial = super().get_initial()
		initial['email'] = self.user_to_edit.email
		initial['first_name'] = self.user_to_edit.first_name
		initial['last_name'] = self.user_to_edit.last_name
		initial['is_active'] = self.user_to_edit.is_active
		
		# Set group
		if self.user_to_edit.groups.exists():
			initial['group'] = self.user_to_edit.groups.first()
		
		# Set profile data
		if hasattr(self.user_to_edit, 'profile'):
			initial['matricula'] = self.user_to_edit.profile.matricula
			initial['unidade'] = self.user_to_edit.profile.unidade
		
		return initial

	def form_valid(self, form):
		user = form.save()
		messages.success(self.request, f"Usuário '{user.username}' atualizado com sucesso!")
		return HttpResponseRedirect(reverse_lazy('accounts:user-list'))

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['page_title'] = f'Editar Usuário: {self.user_to_edit.username}'
		context['user_to_edit'] = self.user_to_edit
		return context


class UserDeleteView(AdminTIRequiredMixin, DeleteView):
	"""View for deleting users."""
	model = User
	template_name = 'accounts/user_confirm_delete.html'
	success_url = reverse_lazy('accounts:user-list')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['user_to_delete'] = self.object
		return context

	def delete(self, request, *args, **kwargs):
		user = self.get_object()
		username = user.username
		messages.success(request, f"Usuário '{username}' excluído com sucesso!")
		return super().delete(request, *args, **kwargs)
