from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, ClientProfile
from django.contrib.auth.models import Group

class ClientProfileInline(admin.StackedInline):
    model = ClientProfile
    can_delete = False
    verbose_name_plural = 'Client Profile'

class CustomUserAdmin(UserAdmin):
    model = User
    inlines = (ClientProfileInline,)
    list_display = ('email', 'first_name', 'last_name', 'national_id', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('email', 'first_name', 'last_name', 'national_id')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'national_id')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password', 'national_id'),
        }),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.unregister(Group)