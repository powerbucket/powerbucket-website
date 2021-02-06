from django.shortcuts import render
from readings.models import Reading, Settings
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.urls import reverse
from django.views import generic
from django.forms.models import model_to_dict

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

from readings.forms import SubmissionForm, SettingsForm
def submission(request):
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
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

def change_settings(request):
    if request.method == 'POST':
        form = SettingsForm(request.POST)
        if form.is_valid():
            new_settings = form.save(commit=False)
            new_settings.user = request.user
            old_settings,created = Settings.objects.update_or_create(user=request.user,
                                                                     defaults={'x': new_settings.x,
                                                                               'y': new_settings.y,
                                                                               'r': new_settings.r,
                                                                               'update': new_settings.update})
            old_settings.save()
            return HttpResponseRedirect('/')
    else:
        form = SettingsForm()
        queryset=Settings.objects.filter(user=request.user.id)
        if queryset.count() != 0:
            old_settings=queryset.first()
            form.fields['x'].initial=old_settings.x
            form.fields['y'].initial=old_settings.y
            form.fields['r'].initial=old_settings.r
            form.fields['update'].initial=old_settings.update
        else:
            form.fields['x'].initial=0
            form.fields['y'].initial=0
            form.fields['r'].initial=0
            form.fields['update'].initial=True

    context = {
        'form': form,
    }

    return render(request, 'change_settings.html', context)


from django.contrib.auth.mixins import LoginRequiredMixin

class SettingsView(LoginRequiredMixin, generic.ListView):
    model = Settings
    def get_queryset(self):
        return Settings.objects.filter(user=self.request.user)

class ReadingView(LoginRequiredMixin, generic.ListView):
    model = Reading
    def get_queryset(self):
        return Reading.objects.filter(user=self.request.user)


def csrf_failure(request, reason="tits"):
    context = {'message': 'some custom messages'}
    return render(request, 'csrf.html', context)
