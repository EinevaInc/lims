from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('survey_realestate/', include('survey_realestate.urls')),
    path('accounts/', include('accounts.urls')),  # Include accounts URLs
    # Add other project-level URLs here
]