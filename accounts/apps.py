from django.apps import AppConfig
from django.db.models.signals import post_migrate


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self) -> None:  # pragma: no cover - side effects only
        from django.apps import apps

        from . import signals  # noqa: F401
        from .mixins import ADMIN_TI_GROUP, GESTOR_GROUP, TECNICO_GROUP

        def ensure_default_groups(sender, **kwargs):  # pragma: no cover - setup task
            group_model = apps.get_model('auth', 'Group')
            for group_name in (GESTOR_GROUP, ADMIN_TI_GROUP, TECNICO_GROUP):
                group_model.objects.get_or_create(name=group_name)

        post_migrate.connect(
            ensure_default_groups,
            sender=self,
            dispatch_uid='accounts.ensure_default_groups',
        )
        return super().ready()
