from django.urls import path
from . import views

app_name = 'accounts'  # Add app_name for namespacing

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.update_profile, name='profile_edit'),
]