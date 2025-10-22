from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Profile

User = get_user_model()


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    fk_name = 'user'
    extra = 0


try:
	admin.site.unregister(User)
except admin.sites.NotRegistered:  # pragma: no cover - defensive branch
	pass


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInline]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'matricula', 'unidade')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'matricula')
    list_filter = ('unidade',)
