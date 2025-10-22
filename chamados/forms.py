import base64
from uuid import uuid4

from django import forms
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile

from .models import Chamado

User = get_user_model()


class BaseTailwindForm(forms.ModelForm):
    """Shared helper to apply Tailwind-friendly classes."""

    def _apply_tailwind_widgets(self) -> None:
        for field in self.fields.values():
            existing = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f"{existing} block w-full rounded border border-slate-300 bg-white px-3 py-2 text-sm shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-400".strip()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_tailwind_widgets()


class ChamadoForm(BaseTailwindForm):
    class Meta:
        model = Chamado
        fields = ['titulo', 'descricao', 'prioridade', 'memorando']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 4}),
        }


class ChamadoAdminUpdateForm(BaseTailwindForm):
    tecnicos_designados = forms.ModelMultipleChoiceField(
        queryset=None,
        required=False,
        widget=forms.SelectMultiple(attrs={'size': 6}),
        label='Técnicos Designados',
    )

    class Meta:
        model = Chamado
        fields = [
            'status',
            'prioridade',
            'notas_resolucao',
            'tecnicos_designados',
            'memorando',
        ]
        widgets = {
            'notas_resolucao': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        tecnico_qs = User.objects.filter(groups__name='Tecnico').order_by('first_name', 'last_name')
        self.fields['tecnicos_designados'].queryset = tecnico_qs


class ChamadoTecnicoUpdateForm(BaseTailwindForm):
    class Meta:
        model = Chamado
        fields = ['status', 'notas_resolucao']
        widgets = {
            'notas_resolucao': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Técnicos só podem mudar para "Em Andamento" ou "Resolvida"
        self.fields['status'].choices = [
            (Chamado.Status.EM_ANDAMENTO, 'Em Andamento'),
            (Chamado.Status.RESOLVIDA, 'Resolvida'),
        ]


class ChamadoFinalizarForm(BaseTailwindForm):
    assinatura_data = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Chamado
        fields = [
            'avaliacao_estrelas',
            'observacao_final',
            'nome_cliente_final',
            'matricula_cliente_final',
        ]
        widgets = {
            'observacao_final': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_assinatura_data(self):
        data = self.cleaned_data.get('assinatura_data')
        if not data:
            raise forms.ValidationError('A assinatura é obrigatória.')
        if not data.startswith('data:image'):
            raise forms.ValidationError('Formato de assinatura inválido.')
        return data

    def build_assinatura_file(self):
        data = self.cleaned_data['assinatura_data']
        try:
            header, encoded = data.split(';base64,')
        except ValueError as exc:  # pragma: no cover - defensive
            raise forms.ValidationError('Não foi possível ler a assinatura enviada.') from exc
        file_ext = header.split('/')[-1]
        content = ContentFile(base64.b64decode(encoded), name=f"assinatura-{uuid4().hex}.{file_ext}")
        return content
