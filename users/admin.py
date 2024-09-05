from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.sessions.models import Session

from .models import *


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        ('User Credentials', {
            'fields': ('email', 'password', 'first_name', 'last_name', 'full_name', 'phone_number',)
        }),
        ('User Groups', {
            'fields': ('groups',)
        }),
        ('Basic', {
            'fields': ('date_of_birth',
                       'user_image', 'role', 'is_staff', 'is_active', 'date_joined', 'created_by', 'modified_by',
                       'modified_datetime',)
        }),
    )
    readonly_fields = ['date_joined']


# Register your models here.
admin.site.register(User, CustomUserAdmin)
admin.site.register(Session)
admin.site.register(UserPermissions)
