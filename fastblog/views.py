from django.shortcuts import render # type: ignore
from django.views import generic # type: ignore
from .models import Fasting_Plan

# Create your views here.
def home(request):
    return render(request, 'fastblog/home.html')


class FastingPlanListView(generic.ListView):

    queryset = Fasting_Plan.objects.all()
    template_name = 'fastblog/fast_list.html'
    