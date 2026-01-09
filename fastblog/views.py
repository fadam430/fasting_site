from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
from django.views import generic # type: ignore
from django.http import HttpResponseNotAllowed # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.contrib.auth import login # type: ignore
from django.contrib.auth.models import User # type: ignore
from .models import Fasting_Plan, Reviews
from .forms import RegistrationForm
from .forms import ReviewForm
from django.http import HttpResponseForbidden

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


@login_required
def edit_review(request, pk):
    review = get_object_or_404(Reviews, pk=pk)
    if not (request.user == review.reviewer or request.user.is_staff):
        return HttpResponseForbidden('Not allowed')

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review.rating = form.cleaned_data['rating']
            review.comment = form.cleaned_data['comment']
            review.save()
            return redirect('fasting_list')
    else:
        form = ReviewForm(initial={'rating': review.rating, 'comment': review.comment})

    return render(request, 'fastblog/review_edit.html', {'form': form, 'review': review})


@login_required
def delete_review(request, pk):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    review = get_object_or_404(Reviews, pk=pk)
    if not (request.user == review.reviewer or request.user.is_staff):
        return HttpResponseForbidden('Not allowed')
    review.delete()
    return redirect('fasting_list')
