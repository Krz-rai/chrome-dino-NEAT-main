# Description: This file contains the URL patterns for the Core app.
from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    ForgotPassword,
    PasswordResetSent,
    ResetPassword,
    quiz_list_view,
    home,
    quiz_main,
    results,
    profile_view
)
from . import views


urlpatterns = [
    path('', home, name='home'), 
    path('quiz-list/', quiz_list_view, name='quiz_list'),
    path('api/quiz/', quiz_list_view, name='quiz_list_api'),
    path('register/', RegisterView, name='register'),
    path('login/', LoginView, name='login'),
    path('logout/', LogoutView, name='logout'),
    path('forgot-password/', ForgotPassword, name='forgot-password'),
    path('password-reset-sent/<str:reset_id>/', PasswordResetSent, name='password-reset-sent'),
    path('reset-password/<str:reset_id>/', ResetPassword, name='reset-password'),
    path('quiz_main/', quiz_main, name = 'quiz_main'),
    path('results/', results, name='results'),
    path('profile/', profile_view, name='profile'),
    path('profile/update/', profile_view, name='update_profile'),  # Add this line
    path('save_quiz_results/', views.save_quiz_results, name='save_quiz_results'),
    path('results/', views.results, name='results'),
    path('save_quiz_results/', views.save_quiz_results, name='save_quiz_results'),
]
