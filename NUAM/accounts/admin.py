from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    list_display = ("username", "email", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")

    fieldsets = (
        ("Información de usuario", {
            "fields": ("username", "password", "email")
        }),
        ("Datos personales", {
            "fields": ("first_name", "last_name")
        }),
        ("Rol y permisos", {
            "fields": ("role", "is_staff", "is_active", "is_superuser",
                       "groups", "user_permissions")
        }),
        ("Fechas importantes", {
            "fields": ("last_login", "date_joined")
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2", "role", "is_staff", "is_active"),
        }),
    )
