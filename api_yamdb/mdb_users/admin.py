from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (
            'Личная информация',
            {
                'fields': ('first_name', 'last_name', 'email', 'bio'),
                'description': 'Личная информация',
            },
        ),
        (
            'Права доступа',
            {
                'fields': (
                    'role',
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                ),
                'description': 'Права доступа',
            },
        ),
        (
            'Дата входа и регистрации',
            {
                'fields': ('last_login', 'date_joined'),
                'description': 'Дата последнего входа и регистрации',
            },
        ),
        (
            'Дополнительно',
            {
                'fields': ('confirmation_code',),
                'classes': ('collapse',),
                'description': 'Код подтверждения регистрации',
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('username', 'email', 'password1', 'password2'),
            },
        ),
        (
            'Дополнительная информация',
            {
                'classes': ('wide',),
                'fields': ('first_name', 'last_name', 'role', 'bio'),
            },
        ),
    )

    list_display = (
        'username',
        'email',
        'role',
        'is_staff',
        'is_active',
        'date_joined',
    )
    list_filter = ('role', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    readonly_fields = ('date_joined', 'last_login')
