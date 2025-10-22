from django.contrib.auth.mixins import UserPassesTestMixin

GESTOR_GROUP = 'Gestor'
ADMIN_TI_GROUP = 'Administrador TI'
TECNICO_GROUP = 'Tecnico'


class GroupRequiredMixin(UserPassesTestMixin):
    required_groups: tuple[str, ...] = ()
    allow_staff = True

    def test_func(self):
        user = self.request.user
        if not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        if self.allow_staff and user.is_staff:
            return True
        return any(user.groups.filter(name=group).exists() for group in self.required_groups)

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        from django.core.exceptions import PermissionDenied

        raise PermissionDenied("Você não tem permissão para acessar esta página.")


class GestorRequiredMixin(GroupRequiredMixin):
    required_groups = (GESTOR_GROUP,)
    allow_staff = False


class AdminTIRequiredMixin(GroupRequiredMixin):
    required_groups = (ADMIN_TI_GROUP,)


class TecnicoRequiredMixin(GroupRequiredMixin):
    required_groups = (TECNICO_GROUP,)
    allow_staff = False
