from . import views
from django.urls import path # type: ignore

urlpatterns = [
    path('', views.FastingPlanListView.as_view(), name='fasting_list'),
]