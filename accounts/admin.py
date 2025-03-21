from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, ClientProfile
from django.contrib.auth.models import Group


class ClientProfileInline(admin.StackedInline):  # Or admin.TabularInline
    """
    Allows editing ClientProfile inline in the User admin.
    """
    model = ClientProfile
    can_delete = False  # Prevent deleting the profile from the User admin
    verbose_name_plural = 'Client Profile'


class CustomUserAdmin(UserAdmin):
    """
    Customizes the User admin to use the custom User model and include ClientProfile.
    """
    model = User
    inlines = (ClientProfileInline,)  # Add the inline for ClientProfile
    list_display = ('email', 'first_name', 'last_name', 'national_id', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('email', 'first_name', 'last_name', 'national_id')
    ordering = ('email',)

    fieldsets = (  # Customize the fields displayed in the admin edit form
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'national_id')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = ( # Add custom fields
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password', 'national_id'),
        }),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.unregister(Group) # Unregisters the default group.