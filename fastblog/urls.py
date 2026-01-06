from . import views
from django.urls import path

urlpatterns = [
    path('', views.FastingPlanListView.as_view(), name='home'),
]