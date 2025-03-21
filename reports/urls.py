from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('property_listing/', views.PropertyListingReportView.as_view(), name='property_listing'),
    # Add other report URLs here
]
