from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from chamados.models import Chamado, Unidade


class Command(BaseCommand):
	help = 'Create default groups: Gestor, Tecnico, and Administrador TI, and default Unidade'

	def handle(self, *args, **options):
		# Create default Unidade if none exists
		if not Unidade.objects.exists():
			unidade, created = Unidade.objects.get_or_create(nome='Sede Principal')
			if created:
				self.stdout.write(self.style.SUCCESS('✓ Unidade padrão "Sede Principal" criada'))
			else:
				self.stdout.write(self.style.WARNING('→ Unidade "Sede Principal" já existe'))
		else:
			self.stdout.write(self.style.SUCCESS(f'→ {Unidade.objects.count()} unidade(s) já cadastrada(s)'))

		groups_data = {
			'Gestor': {
				'permissions': [
					'add_chamado',
					'change_chamado',
					'view_chamado',
				]
			},
			'Tecnico': {
				'permissions': [
					'view_chamado',
					'change_chamado',
				]
			},
			'Administrador TI': {
				'permissions': [
					'add_chamado',
					'change_chamado',
					'delete_chamado',
					'view_chamado',
					'add_unidade',
					'change_unidade',
					'delete_unidade',
					'view_unidade',
				]
			},
		}

		for group_name, group_data in groups_data.items():
			group, created = Group.objects.get_or_create(name=group_name)
			if created:
				self.stdout.write(self.style.SUCCESS(f'✓ Grupo "{group_name}" criado'))
			else:
				self.stdout.write(self.style.WARNING(f'→ Grupo "{group_name}" já existe'))

			# Add permissions to group
			for permission_codename in group_data['permissions']:
				try:
					# Try to find permission in Chamado model
					permission = Permission.objects.get(
						codename=permission_codename,
						content_type=ContentType.objects.get_for_model(Chamado)
					)
					group.permissions.add(permission)
				except Permission.DoesNotExist:
					# Try to find in other models
					try:
						permission = Permission.objects.get(codename=permission_codename)
						group.permissions.add(permission)
					except Permission.DoesNotExist:
						self.stdout.write(
							self.style.WARNING(f'  ⚠ Permissão "{permission_codename}" não encontrada')
						)

		self.stdout.write(
			self.style.SUCCESS('\n✓ Inicialização de grupos e unidades concluída com sucesso!')
		)
