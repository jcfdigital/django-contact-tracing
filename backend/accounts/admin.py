from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin

from . import models

@admin.register(models.AccountsModel)
class AccountsModelAdmin(UserAdmin):
    
    model = models.AccountsModel

    list_display = (
        'email',
        'time_created',
        'time_updated',
        'is_active',
        'is_staff',
        'is_superuser',
    )

    list_filter = (
        ('is_active', admin.BooleanFieldListFilter),
        ('is_staff', admin.BooleanFieldListFilter),
        ('is_superuser', admin.BooleanFieldListFilter),
    )
    
    readonly_fields = (
        'time_created',
        'time_updated',
    )

    search_fields = (
        'email',
    )

    ordering = ('id', )

    fieldsets = (
        ('Credentials', {'fields': ('email', 'password',)}),
        ('Permissions', {'fields': ('is_active','is_staff','is_superuser',)}),
        ('Others', {'fields': ('time_created','time_updated',)}),
    )

    add_fieldsets = (
        ('Credentials', {'fields': ('email', 'password1','password2')}),
        ('Permissions', {'fields': ('is_active','is_staff','is_superuser',)}),
    )

admin.site.unregister(Group)