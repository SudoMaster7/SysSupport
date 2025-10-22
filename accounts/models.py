from django.conf import settings
from django.db import models


class Profile(models.Model):
	user = models.OneToOneField(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name='profile',
	)
	matricula = models.CharField(max_length=100, blank=True, null=True)
	unidade = models.ForeignKey(
		'chamados.Unidade',
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
		related_name='profiles',
	)

	def __str__(self) -> str:  # pragma: no cover - simple representation
		return f"Perfil de {self.user.get_full_name() or self.user.username}"
