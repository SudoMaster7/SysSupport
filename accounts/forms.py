from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from .models import Profile
from chamados.models import Unidade

User = get_user_model()


class BaseTailwindForm(forms.Form):
    """Base form class with Tailwind CSS styling."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_tailwind_classes()

    def apply_tailwind_classes(self):
        for field_name, field in self.fields.items():
            field.widget.attrs.update(
                {
                    "class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                }
            )
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({"class": field.widget.attrs["class"] + " bg-white"})
            if isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update(
                    {
                        "class": "form-checkbox h-4 w-4 text-blue-600 rounded focus:ring-blue-500"
                    }
                )


class UserCreateForm(forms.Form):
    """Form for creating users with group and profile assignment."""

    username = forms.CharField(
        max_length=150,
        label="Nome de Usuário",
        widget=forms.TextInput(attrs={"placeholder": "Ex: joao.silva", "class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"}),
    )
    email = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(attrs={"placeholder": "Ex: joao@example.com", "class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"}),
    )
    first_name = forms.CharField(
        max_length=150,
        label="Nome",
        widget=forms.TextInput(attrs={"placeholder": "Ex: João", "class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"}),
    )
    last_name = forms.CharField(
        max_length=150,
        label="Sobrenome",
        widget=forms.TextInput(attrs={"placeholder": "Ex: Silva", "class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"}),
    )
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={"placeholder": "Digite uma senha segura", "class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"}),
    )
    password_confirm = forms.CharField(
        label="Confirmar Senha",
        widget=forms.PasswordInput(attrs={"placeholder": "Confirme a senha", "class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"}),
    )
    group = forms.ModelChoiceField(
        queryset=Group.objects.filter(name__in=["Gestor", "Tecnico"]),
        label="Perfil (Grupo)",
        widget=forms.RadioSelect(),
    )
    matricula = forms.CharField(
        max_length=100,
        label="Matrícula",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Ex: MAT001", "class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"}),
    )
    unidade = forms.ModelChoiceField(
        queryset=Unidade.objects.all(),
        label="Unidade",
        required=True,
        widget=forms.Select(attrs={"class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white"}),
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            self.add_error("password_confirm", "As senhas não conferem.")

        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nome de usuário já está em uso.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este e-mail já está em uso.")
        return email

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data["username"],
            email=self.cleaned_data["email"],
            first_name=self.cleaned_data["first_name"],
            last_name=self.cleaned_data["last_name"],
            password=self.cleaned_data["password"],
        )

        # Add user to group
        group = self.cleaned_data["group"]
        user.groups.add(group)

        # Create/update profile
        profile, _ = Profile.objects.get_or_create(user=user)
        profile.matricula = self.cleaned_data.get("matricula", "")
        profile.unidade = self.cleaned_data["unidade"]
        if commit:
            profile.save()

        if commit:
            user.save()

        return user


class UserEditForm(forms.Form):
    """Form for editing existing users."""

    email = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(attrs={"placeholder": "Ex: joao@example.com", "class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"}),
    )
    first_name = forms.CharField(
        max_length=150,
        label="Nome",
        widget=forms.TextInput(attrs={"placeholder": "Ex: João", "class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"}),
    )
    last_name = forms.CharField(
        max_length=150,
        label="Sobrenome",
        widget=forms.TextInput(attrs={"placeholder": "Ex: Silva", "class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"}),
    )
    group = forms.ModelChoiceField(
        queryset=Group.objects.filter(name__in=["Gestor", "Tecnico", "Administrador TI"]),
        label="Perfil (Grupo)",
        widget=forms.RadioSelect(),
    )
    matricula = forms.CharField(
        max_length=100,
        label="Matrícula",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Ex: MAT001", "class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"}),
    )
    unidade = forms.ModelChoiceField(
        queryset=Unidade.objects.all(),
        label="Unidade",
        required=True,
        widget=forms.Select(attrs={"class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white"}),
    )
    is_active = forms.BooleanField(
        label="Usuário ativo",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "h-4 w-4 text-blue-600 rounded focus:ring-blue-500"}),
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exclude(pk=self.user.pk).exists():
            raise forms.ValidationError("Este e-mail já está em uso.")
        return email

    def save(self, commit=True):
        if not self.user:
            raise ValueError("User instance is required for editing")

        self.user.email = self.cleaned_data["email"]
        self.user.first_name = self.cleaned_data["first_name"]
        self.user.last_name = self.cleaned_data["last_name"]
        self.user.is_active = self.cleaned_data.get("is_active", True)

        # Update groups
        self.user.groups.clear()
        group = self.cleaned_data["group"]
        self.user.groups.add(group)

        # Update profile
        profile, _ = Profile.objects.get_or_create(user=self.user)
        profile.matricula = self.cleaned_data.get("matricula", "")
        profile.unidade = self.cleaned_data["unidade"]

        if commit:
            self.user.save()
            profile.save()

        return self.user
