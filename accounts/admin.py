from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("school_name","email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "school_name","password1", "password2"),
        }),
    )
    list_display = ("email", "school_name", "is_active","is_staff")
    search_fields = ("email", "school_name")
    ordering = ("email",)

admin.site.register(User, CustomUserAdmin)