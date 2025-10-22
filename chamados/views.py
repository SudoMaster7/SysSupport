from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, FormView, UpdateView

from accounts.mixins import AdminTIRequiredMixin, GestorRequiredMixin, TecnicoRequiredMixin

from .forms import (
	ChamadoAdminUpdateForm,
	ChamadoFinalizarForm,
	ChamadoForm,
	ChamadoTecnicoUpdateForm,
)
from .models import Chamado, Unidade


class ChamadoListView(LoginRequiredMixin, ListView):
	model = Chamado
	template_name = 'chamados/chamado_list.html'
	context_object_name = 'chamados'
	paginate_by = 10

	def get_queryset(self):
		queryset = (
			super()
			.get_queryset()
			.select_related('unidade', 'solicitante')
			.prefetch_related('tecnicos_designados')
		)
		user = self.request.user
		status = self.request.GET.get('status')
		prioridade = self.request.GET.get('prioridade')
		unidade = self.request.GET.get('unidade')

		if (
			not user.groups.filter(name='Administrador TI').exists()
			and not user.is_staff
			and not user.is_superuser
		):
			if user.groups.filter(name='Tecnico').exists():
				queryset = queryset.filter(tecnicos_designados=user)
			else:
				queryset = queryset.filter(solicitante=user)

		if status:
			queryset = queryset.filter(status=status)
		if prioridade:
			queryset = queryset.filter(prioridade=prioridade)
		if unidade:
			queryset = queryset.filter(unidade_id=unidade)

		return queryset

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['status_choices'] = Chamado.Status.choices
		context['prioridade_choices'] = Chamado.Prioridade.choices
		context['unidades'] = Unidade.objects.all()
		context['is_admin_ti'] = (
			self.request.user.groups.filter(name='Administrador TI').exists()
			or self.request.user.is_staff
			or self.request.user.is_superuser
		)
		context['is_gestor'] = self.request.user.groups.filter(name='Gestor').exists()
		return context


class ChamadoDetailView(LoginRequiredMixin, DetailView):
	model = Chamado
	template_name = 'chamados/chamado_detail.html'
	context_object_name = 'chamado'

	def dispatch(self, request, *args, **kwargs):
		self.object = self.get_object()
		chamado = self.object
		user = request.user
		if (
			user.is_superuser
			or user.is_staff
			or user.groups.filter(name='Administrador TI').exists()
		):
			return super().dispatch(request, *args, **kwargs)
		if chamado.solicitante == user or chamado.tecnicos_designados.filter(pk=user.pk).exists():
			return super().dispatch(request, *args, **kwargs)
		return HttpResponseForbidden('Você não tem acesso a este chamado.')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['can_finalize'] = self.object.pode_ser_finalizado_por(self.request.user)
		context['is_admin_ti'] = (
			self.request.user.groups.filter(name='Administrador TI').exists()
			or self.request.user.is_staff
			or self.request.user.is_superuser
		)
		context['is_tecnico'] = (
			self.object.tecnicos_designados.filter(pk=self.request.user.pk).exists()
			and self.object.status != Chamado.Status.FECHADA
		)
		return context


class ChamadoCreateView(GestorRequiredMixin, CreateView):
	model = Chamado
	form_class = ChamadoForm
	template_name = 'chamados/chamado_form.html'
	success_url = reverse_lazy('chamados:lista')

	def form_valid(self, form):
		chamado = form.save(commit=False)
		chamado.solicitante = self.request.user
		profile = getattr(self.request.user, 'profile', None)
		if profile and profile.unidade:
			chamado.unidade = profile.unidade
		else:
			messages.error(
				self.request,
				'Associe seu perfil a uma unidade antes de abrir chamados.',
			)
			return redirect('accounts:profile-detail')
		chamado.save()
		form.save_m2m()
		messages.success(self.request, 'Chamado criado com sucesso!')
		self.object = chamado
		return redirect(self.get_success_url())


class ChamadoAdminUpdateView(AdminTIRequiredMixin, UpdateView):
	model = Chamado
	form_class = ChamadoAdminUpdateForm
	template_name = 'chamados/chamado_update_form.html'
	success_url = reverse_lazy('chamados:lista')

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs['request'] = self.request
		return kwargs

	def form_valid(self, form):
		response = super().form_valid(form)
		messages.success(self.request, 'Chamado atualizado com sucesso!')
		return response


class ChamadoTecnicoUpdateView(LoginRequiredMixin, UpdateView):
	model = Chamado
	form_class = ChamadoTecnicoUpdateForm
	template_name = 'chamados/chamado_tecnico_update_form.html'

	def dispatch(self, request, *args, **kwargs):
		self.object = self.get_object()
		chamado = self.object
		user = request.user
		
		# Verificar se o usuário é técnico designado para este chamado
		if not chamado.tecnicos_designados.filter(pk=user.pk).exists():
			return HttpResponseForbidden('Você não está designado para este chamado.')
		
		# Verificar se o chamado já está fechado
		if chamado.status == Chamado.Status.FECHADA:
			messages.warning(request, 'Este chamado já está fechado e não pode ser alterado.')
			return redirect('chamados:detalhe', pk=chamado.pk)
		
		return super().dispatch(request, *args, **kwargs)

	def get_success_url(self):
		return reverse_lazy('chamados:detalhe', kwargs={'pk': self.object.pk})

	def form_valid(self, form):
		response = super().form_valid(form)
		messages.success(self.request, 'Status do chamado atualizado com sucesso!')
		return response


class ChamadoFinalizarView(GestorRequiredMixin, FormView):
	template_name = 'chamados/chamado_finalizar_form.html'
	form_class = ChamadoFinalizarForm

	def dispatch(self, request, *args, **kwargs):
		self.chamado = get_object_or_404(Chamado, pk=kwargs['pk'])
		if not self.chamado.pode_ser_finalizado_por(request.user):
			return HttpResponseForbidden('Você não pode finalizar este chamado.')
		return super().dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['chamado'] = self.chamado
		return context

	def form_valid(self, form):
		assinatura_file = form.build_assinatura_file()
		self.chamado.registrar_finalizacao(
			estrelas=form.cleaned_data['avaliacao_estrelas'],
			observacao=form.cleaned_data.get('observacao_final'),
			nome_cliente=form.cleaned_data['nome_cliente_final'],
			matricula_cliente=form.cleaned_data['matricula_cliente_final'],
			assinatura_imagem=assinatura_file,
		)
		messages.success(self.request, 'Chamado finalizado com sucesso!')
		return redirect('chamados:detalhe', pk=self.chamado.pk)


class TempoEsperaAPIView(LoginRequiredMixin, View):
	def get(self, request, *args, **kwargs):
		queryset = Chamado.objects.all()
		if (
			not request.user.groups.filter(name='Administrador TI').exists()
			and not request.user.is_staff
		):
			queryset = queryset.filter(solicitante=request.user)
		data = [
			{
				'id': chamado.id,
				'tempo_espera_minutos': round(
					chamado.tempo_espera.total_seconds() / 60,
					2,
				),
			}
			for chamado in queryset
		]
		return JsonResponse({'items': data})
