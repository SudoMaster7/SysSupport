import base64
from uuid import uuid4

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.contrib.auth.models import Group
from rest_framework import serializers

from .models import Chamado, Unidade

User = get_user_model()


class UnidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unidade
        fields = ['id', 'nome']


class ChamadoSerializer(serializers.ModelSerializer):
    solicitante = serializers.StringRelatedField(read_only=True)
    unidade_nome = serializers.CharField(source='unidade.nome', read_only=True)
    tempo_espera_minutos = serializers.SerializerMethodField()
    tecnicos_designados = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.filter(groups__name='Tecnico'),
        required=False,
    )

    class Meta:
        model = Chamado
        fields = [
            'id',
            'titulo',
            'descricao',
            'status',
            'prioridade',
            'data_abertura',
            'data_fechamento',
            'solicitante',
            'unidade',
            'unidade_nome',
            'tecnicos_designados',
            'memorando',
            'notas_resolucao',
            'avaliacao_estrelas',
            'observacao_final',
            'nome_cliente_final',
            'matricula_cliente_final',
            'assinatura',
            'tempo_espera_minutos',
        ]
        read_only_fields = [
            'status',
            'data_abertura',
            'data_fechamento',
            'solicitante',
            'notas_resolucao',
            'avaliacao_estrelas',
            'observacao_final',
            'nome_cliente_final',
            'matricula_cliente_final',
            'assinatura',
        ]
        extra_kwargs = {
            'unidade': {'required': False},
        }

    def get_tempo_espera_minutos(self, obj: Chamado) -> float:
        return round(obj.tempo_espera.total_seconds() / 60, 2)

    def create(self, validated_data):
        request = self.context['request']
        validated_data['solicitante'] = request.user
        tecnicos = validated_data.pop('tecnicos_designados', [])
        unidade = validated_data.get('unidade')
        profile = getattr(request.user, 'profile', None)
        if not unidade:
            if profile and profile.unidade:
                validated_data['unidade'] = profile.unidade
            else:
                raise serializers.ValidationError('O solicitante precisa estar associado a uma unidade.')
        chamado = Chamado.objects.create(**validated_data)
        if tecnicos:
            chamado.tecnicos_designados.set(tecnicos)
        return chamado


class ChamadoUpdateSerializer(serializers.ModelSerializer):
    tecnicos_designados = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.filter(groups__name='Tecnico'),
        required=False,
    )

    class Meta:
        model = Chamado
        fields = ['status', 'prioridade', 'notas_resolucao', 'tecnicos_designados', 'memorando']

    def update(self, instance, validated_data):
        tecnicos = validated_data.pop('tecnicos_designados', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if tecnicos is not None:
            instance.tecnicos_designados.set(tecnicos)
        return instance


class ChamadoFinalizarSerializer(serializers.Serializer):
    avaliacao_estrelas = serializers.ChoiceField(choices=[(i, i) for i in range(1, 6)])
    observacao_final = serializers.CharField(allow_blank=True, required=False)
    nome_cliente_final = serializers.CharField()
    matricula_cliente_final = serializers.CharField()
    assinatura = serializers.CharField()

    def save(self, chamado: Chamado):
        data = self.validated_data
        assinatura_data = data['assinatura']
        if not assinatura_data.startswith('data:image'):
            raise serializers.ValidationError('Assinatura inválida.')
        try:
            header, encoded = assinatura_data.split(';base64,')
        except ValueError as exc:  # pragma: no cover - defensive
            raise serializers.ValidationError('Assinatura inválida.') from exc
        ext = header.split('/')[-1]
        content = ContentFile(base64.b64decode(encoded), name=f"assinatura-{uuid4().hex}.{ext}")
        chamado.registrar_finalizacao(
            estrelas=data['avaliacao_estrelas'],
            observacao=data.get('observacao_final'),
            nome_cliente=data['nome_cliente_final'],
            matricula_cliente=data['matricula_cliente_final'],
            assinatura_imagem=content,
        )
        return chamado


class UserSerializer(serializers.ModelSerializer):
    groups = serializers.SlugRelatedField(many=True, slug_field='name', queryset=Group.objects.all(), required=False)

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'groups']
        read_only_fields = ['id']


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    groups = serializers.SlugRelatedField(many=True, slug_field='name', queryset=Group.objects.all())

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'groups']

    def create(self, validated_data):
        groups = validated_data.pop('groups', [])
        user = get_user_model().objects.create_user(**validated_data)
        if groups:
            user.groups.set(groups)
        return user
