from . import views
from django.urls import path # type: ignore

urlpatterns = [
    path('', views.FastingPlanListView.as_view(), name='fasting_list'),
    path('review/add/', views.add_review, name='add_review'),
    path('register/', views.register, name='register'),
]