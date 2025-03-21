from django.urls import path
from . import views

app_name = 'survey_realestate'  # Add app_name for namespacing

urlpatterns = [
    path('properties/', views.PropertyListView.as_view(), name='property_list'),
    path('properties/<int:pk>/', views.PropertyDetailView.as_view(), name='property_detail'),
    path('properties/create/', views.PropertyCreateView.as_view(), name='property_create'),
    path('properties/<int:pk>/update/', views.PropertyUpdateView.as_view(), name='property_update'),
    path('properties/<int:pk>/delete/', views.PropertyDeleteView.as_view(), name='property_delete'),
    path('address/create/', views.AddressCreateView.as_view(), name='address_create'),
    path('property_address/create/', views.create_property_with_address, name='create_property_with_address'),
]