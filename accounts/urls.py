from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.Register.as_view(), name='register'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('forgotpassword', views.forgotpassword, name='forgotpassword'),
    path('resetPassword_validate/<uidb64>/<token>/',
         views.resetPassword_validate, name='resetPassword_validate'),
    path('resetPassword', views.resetPassword, name='resetPassword'),
]
