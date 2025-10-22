from django.conf import settings
from django.db import models
from django.utils import timezone

User = settings.AUTH_USER_MODEL


class Unidade(models.Model):
	nome = models.CharField(max_length=255, unique=True)

	class Meta:
		ordering = ['nome']

	def __str__(self) -> str:  # pragma: no cover - simple representation
		return self.nome


class Chamado(models.Model):
	class Status(models.TextChoices):
		ABERTA = 'Aberta', 'Aberta'
		EM_ANDAMENTO = 'Em Andamento', 'Em Andamento'
		RESOLVIDA = 'Resolvida', 'Resolvida'
		FECHADA = 'Fechada', 'Fechada'

	class Prioridade(models.TextChoices):
		BAIXA = 'Baixa', 'Baixa'
		MEDIA = 'Média', 'Média'
		ALTA = 'Alta', 'Alta'
		CRITICA = 'Crítica', 'Crítica'

	titulo = models.CharField(max_length=255)
	descricao = models.TextField()
	status = models.CharField(
		max_length=50,
		choices=Status.choices,
		default=Status.ABERTA,
	)
	prioridade = models.CharField(
		max_length=20,
		choices=Prioridade.choices,
		default=Prioridade.MEDIA,
	)
	data_abertura = models.DateTimeField(auto_now_add=True)
	data_fechamento = models.DateTimeField(null=True, blank=True)
	solicitante = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='chamados_abertos',
	)
	unidade = models.ForeignKey(
		Unidade,
		on_delete=models.CASCADE,
		related_name='chamados',
	)
	tecnicos_designados = models.ManyToManyField(
		User,
		related_name='chamados_designados',
		blank=True,
	)
	memorando = models.FileField(upload_to='memorandos/', null=True, blank=True)
	notas_resolucao = models.TextField(null=True, blank=True)
	avaliacao_estrelas = models.IntegerField(
		choices=[(i, i) for i in range(1, 6)],
		null=True,
		blank=True,
	)
	observacao_final = models.TextField(null=True, blank=True)
	nome_cliente_final = models.CharField(max_length=255, null=True, blank=True)
	matricula_cliente_final = models.CharField(max_length=100, null=True, blank=True)
	assinatura = models.ImageField(upload_to='assinaturas/', null=True, blank=True)

	class Meta:
		ordering = ['-data_abertura']

	def __str__(self) -> str:  # pragma: no cover - simple representation
		return f"{self.titulo} ({self.get_status_display()})"

	@property
	def tempo_espera(self):
		referencial = self.data_fechamento or timezone.now()
		return referencial - self.data_abertura

	def pode_ser_finalizado_por(self, usuario) -> bool:
		return (
			usuario == self.solicitante
			and self.status == self.Status.RESOLVIDA
		)

	def registrar_finalizacao(
		self,
		estrelas: int,
		observacao: str | None,
		nome_cliente: str,
		matricula_cliente: str,
		assinatura_imagem,
	) -> None:
		self.avaliacao_estrelas = estrelas
		self.observacao_final = observacao
		self.nome_cliente_final = nome_cliente
		self.matricula_cliente_final = matricula_cliente
		if assinatura_imagem:
			self.assinatura = assinatura_imagem
		self.status = self.Status.FECHADA
		self.data_fechamento = timezone.now()
		self.save(update_fields=[
			'avaliacao_estrelas',
			'observacao_final',
			'nome_cliente_final',
			'matricula_cliente_final',
			'assinatura',
			'status',
			'data_fechamento',
		])

# Create your models here.
