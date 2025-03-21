from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin, Group
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    national_id = models.CharField(max_length=20, blank=True, null=True, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client_profile')
    contact_details = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.email}"

# ---Groups and Permissions ----
# Create groups based on the image.
def create_groups():
     # Define the groups and their permissions
    groups_permissions = {
        'Survey-RealEstate': {
            'property': ['add', 'change', 'delete', 'view'],  # Full CRUD on Property
            # Add other permissions as needed
        },
        'Sales': {
            'property': ['view', 'change'], # Can view and edit (but not create or delete)
             'offerletter': ['add', 'change', 'delete', 'view'],
            # Add other permissions
        },
        'Finance': {
            'propertyownership': ['add', 'change', 'delete', 'view'], #manage ownership
            'payment': ['add', 'change', 'delete', 'view'],  # Manage payments
            'invoice': ['add', 'change', 'delete', 'view'],
            'receipt': ['add', 'change', 'delete', 'view'],
            # Add other permissions
        },
         'Clients':{
             'property': ['view'],
             'payment': ['view'],
             'receipt': ['view'],
             # can make payments, uploads, and get receipts.
         }
    }

    for group_name, permissions in groups_permissions.items():
        group, created = Group.objects.get_or_create(name=group_name) # Creates the group
        for model_name, perms in permissions.items():
            for perm_code in perms:
                # Construct the full permission codename
                codename = f'{perm_code}_{model_name}'
                try:
                    # Get the Permission object
                    permission = Permission.objects.get(codename=codename)
                    # Assign the permission to the group
                    group.permissions.add(permission)
                except Permission.DoesNotExist:
                    print(f"Permission {codename} does not exist.")