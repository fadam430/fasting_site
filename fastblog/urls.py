from . import views
from django.urls import path # type: ignore
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.FastingPlanListView.as_view(), name='fasting_list'),
    path('review/add/', views.add_review, name='add_review'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='fastblog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    # Password reset flow
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='fastblog/password_reset_form.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='fastblog/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='fastblog/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='fastblog/password_reset_complete.html'), name='password_reset_complete'),

    path('review/edit/<int:pk>/', views.edit_review, name='edit_review'),
    path('review/delete/<int:pk>/', views.delete_review, name='delete_review'),
]