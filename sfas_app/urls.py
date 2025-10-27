from django.shortcuts import render
from django.urls import path
from . import views


from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('feedback_success/', views.feedback_success, name='feedback_success'),
    path('aboutus/', views.aboutus, name='aboutus'),
    
      path('download_feedbacks/<str:file_format>/', views.download_feedbacks, name='download_feedbacks'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
]
