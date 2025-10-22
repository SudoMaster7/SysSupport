import base64
from io import BytesIO

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.files.base import ContentFile
from django.test import TestCase
from django.urls import reverse
from PIL import Image
from rest_framework.test import APIClient

from accounts.mixins import ADMIN_TI_GROUP, GESTOR_GROUP, TECNICO_GROUP
from accounts.models import Profile
from .models import Chamado, Unidade


def create_signature_image() -> str:
    image = Image.new('RGB', (4, 4), color='black')
    buffer = BytesIO()
    image.save(buffer, format='PNG')
    b64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return f'data:image/png;base64,{b64}'


class TestChamadoModel(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user('gestor', 'gestor@example.com', 'test1234')
        self.unidade = Unidade.objects.create(nome='Campus A')
        profile = self.user.profile
        profile.unidade = self.unidade
        profile.save()

    def test_registrar_finalizacao_updates_fields(self):
        chamado = Chamado.objects.create(
            titulo='Teste',
            descricao='Descricao',
            solicitante=self.user,
            unidade=self.unidade,
        )
        chamado.status = Chamado.Status.RESOLVIDA
        chamado.save()

        assinatura_content = ContentFile(b'fake-image', name='assinatura.png')
        chamado.registrar_finalizacao(
            estrelas=5,
            observacao='Excelente atendimento',
            nome_cliente='Cliente',
            matricula_cliente='123',
            assinatura_imagem=assinatura_content,
        )

        chamado.refresh_from_db()
        self.assertEqual(chamado.status, Chamado.Status.FECHADA)
        self.assertIsNotNone(chamado.data_fechamento)
        self.assertEqual(chamado.avaliacao_estrelas, 5)


class TestChamadoAPI(TestCase):
    def setUp(self):
        for group_name in (GESTOR_GROUP, ADMIN_TI_GROUP, TECNICO_GROUP):
            Group.objects.get_or_create(name=group_name)

        self.gestor = get_user_model().objects.create_user('gestor', 'gestor@example.com', 'pwd1234')
        self.admin = get_user_model().objects.create_user('admin', 'admin@example.com', 'pwd1234', is_staff=True)
        self.tecnico = get_user_model().objects.create_user('tecnico', 'tec@example.com', 'pwd1234')

        self.gestor.groups.add(Group.objects.get(name=GESTOR_GROUP))
        self.admin.groups.add(Group.objects.get(name=ADMIN_TI_GROUP))
        self.tecnico.groups.add(Group.objects.get(name=TECNICO_GROUP))

        self.unidade = Unidade.objects.create(nome='Campus A')
        perfil = self.gestor.profile
        perfil.unidade = self.unidade
        perfil.save()

        self.client = APIClient()

    def test_gestor_cria_chamado(self):
        self.client.force_authenticate(self.gestor)
        response = self.client.post(
            reverse('api-chamados-list'),
            data={'titulo': 'Erro no email', 'descricao': 'Nao envia email', 'prioridade': Chamado.Prioridade.MEDIA},
            format='json',
        )
        self.assertEqual(response.status_code, 201)
        chamado = Chamado.objects.get()
        self.assertEqual(chamado.solicitante, self.gestor)
        self.assertEqual(chamado.unidade, self.unidade)

    def test_admin_atualiza_chamado(self):
        chamado = Chamado.objects.create(
            titulo='Teste',
            descricao='Descricao',
            solicitante=self.gestor,
            unidade=self.unidade,
        )
        self.client.force_authenticate(self.admin)
        response = self.client.patch(
            reverse('api-chamados-atualizar', kwargs={'pk': chamado.pk}),
            data={'status': Chamado.Status.EM_ANDAMENTO, 'tecnicos_designados': [self.tecnico.pk]},
            format='json',
        )
        self.assertEqual(response.status_code, 200)
        chamado.refresh_from_db()
        self.assertEqual(chamado.status, Chamado.Status.EM_ANDAMENTO)
        self.assertIn(self.tecnico, chamado.tecnicos_designados.all())

    def test_gestor_finaliza_chamado(self):
        chamado = Chamado.objects.create(
            titulo='Teste',
            descricao='Descricao',
            solicitante=self.gestor,
            unidade=self.unidade,
            status=Chamado.Status.RESOLVIDA,
        )
        self.client.force_authenticate(self.gestor)
        response = self.client.post(
            reverse('api-chamados-finalizar', kwargs={'pk': chamado.pk}),
            data={
                'avaliacao_estrelas': 4,
                'observacao_final': 'Boa recuperação',
                'nome_cliente_final': 'Cliente',
                'matricula_cliente_final': '321',
                'assinatura': create_signature_image(),
            },
            format='json',
        )
        self.assertEqual(response.status_code, 200)
        chamado.refresh_from_db()
        self.assertEqual(chamado.status, Chamado.Status.FECHADA)
