from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'phone', 'region', 'is_guest')}),
        (_('Referral'), {'fields': ('referral_code', 'referred_by')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone', 'password1', 'password2', 'region', 'is_guest'),
        }),
    )
    list_display = ('id', 'email', 'first_name', 'last_name', 'phone', 'region', 'is_guest', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'region', 'is_guest', 'groups')
    search_fields = ('email', 'first_name', 'last_name', 'phone', 'referral_code')
    ordering = ('-date_joined',)
    readonly_fields = ('referral_code',)

    def get_fieldsets(self, request, obj=None):
        # referral_code readonly olsun
        return super().get_fieldsets(request, obj)