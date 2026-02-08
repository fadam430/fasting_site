from . import views
from django.urls import path # type: ignore
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView # type: ignore

urlpatterns = [
    path('', views.FastingPlanListView.as_view(), name='fasting_list'),
    path('review/add/', views.add_review, name='add_review'),
    # Redirect legacy register page to django-allauth signup
    path('register/', RedirectView.as_view(url='/accounts/signup/', permanent=False), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='fastblog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    
    path('review/edit/<int:pk>/', views.edit_review, name='edit_review'),
    path('review/delete/<int:pk>/', views.delete_review, name='delete_review'),
]