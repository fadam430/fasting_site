from django.shortcuts import render
from .models import About

# Create your views here.
def about(request):
    """
    Renders the about page with information from the About model.
    """
    about = About.objects.all()
    return render(request, 'about/about.html', {'about': about})