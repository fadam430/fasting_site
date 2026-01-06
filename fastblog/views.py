from django.shortcuts import render
from django.views import generic
from .models import Fasting_Plan
# Create your views here.
class FastingPlanListView(generic.ListView):

    queryset = Fasting_Plan.objects.all()
    template_name = 'fastblog/fast_list.html' 
    