from django.contrib import admin

from .models import Chamado, Unidade


@admin.register(Unidade)
class UnidadeAdmin(admin.ModelAdmin):
	list_display = ('nome',)
	search_fields = ('nome',)


@admin.register(Chamado)
class ChamadoAdmin(admin.ModelAdmin):
	list_display = (
		'titulo',
		'status',
		'prioridade',
		'unidade',
		'solicitante',
		'data_abertura',
		'data_fechamento',
	)
	list_filter = ('status', 'prioridade', 'unidade')
	search_fields = (
		'titulo',
		'descricao',
		'solicitante__username',
		'solicitante__first_name',
		'solicitante__last_name',
	)
	filter_horizontal = ('tecnicos_designados',)
