from django.shortcuts import render
from readings.models import Reading
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.urls import reverse
from django.views import generic

# Create your views here.
def index(request):
    num_readings = Reading.objects.all().count()
    num_users = User.objects.all().count()

    context = {
        'num_readings': num_readings,
        'num_users': num_users,
    }

    return render(request, 'index.html', context=context)

from readings.forms import UserRegistrationForm
def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['email'], form.cleaned_data['password'])
            user.save()
            return HttpResponseRedirect(reverse('login'))
    else:
        form = UserRegistrationForm()

    context = {
        'form': form,
    }

    return render(request, 'registration.html', context)

from readings.forms import SubmissionForm
def submission(request):
    if request.method == 'POST':
        form = SubmissionForm(request.POST)
        if form.is_valid():
            new_reading = form.save(commit=False)
            new_reading.user = request.user
            new_reading.save()
            return HttpResponseRedirect('/')
    else:
        form = SubmissionForm()

    context = {
        'form': form,
    }
    
    return render(request, 'submission.html', context)

from django.contrib.auth.mixins import LoginRequiredMixin
class ReadingView(LoginRequiredMixin, generic.ListView):
    model = Reading
    def get_queryset(self):
        return Reading.objects.filter(user=self.request.user)
