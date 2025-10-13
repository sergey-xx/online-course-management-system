from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from simple_history.admin import SimpleHistoryAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin, SimpleHistoryAdmin):

    fieldsets = (
        (None, {'fields': ('username', 'password', 'email')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name',)}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Custom Fields'), {'fields': ('role',)}),
    )
    readonly_fields = (
        'last_login',
        'date_joined',
    )
