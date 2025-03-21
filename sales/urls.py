from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    path('property/<int:pk>/update_info/', views.UpdateLandInfoView.as_view(), name='update_land_info'),
    path('property/<int:pk>/offer_letter/', views.GenerateOfferLetterView.as_view(), name='generate_offer_letter'),
    // Add other URLs here
]
