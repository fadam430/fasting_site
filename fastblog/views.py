from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic # type: ignore
from django.http import HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.models import User
from .models import Fasting_Plan, Reviews
from .forms import RegistrationForm

# Create your views here.
def home(request):
    return render(request, 'fastblog/home.html')


class FastingPlanListView(generic.ListView):

    queryset = Fasting_Plan.objects.all()
    template_name = 'fastblog/fast_list.html'
    


@login_required
def add_review(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    plan_id = request.POST.get('plan_id')
    rating = request.POST.get('rating')
    comment = request.POST.get('comment', '').strip()

    plan = get_object_or_404(Fasting_Plan, pk=plan_id)

    try:
        rating_i = int(rating)
    except (TypeError, ValueError):
        rating_i = 0
    if rating_i < 1:
        rating_i = 1
    if rating_i > 5:
        rating_i = 5

    Reviews.objects.create(
        fasting_plan=plan,
        reviewer=request.user,
        rating=rating_i,
        comment=comment,
    )

    # redirect back to the fasting list page
    return redirect('fasting_list')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'fastblog/register.html', {'form': form})
