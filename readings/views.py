from django.shortcuts import render
from readings.models import Reading, Settings
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.urls import reverse
from django.views import generic
from django.forms.models import model_to_dict

import datetime

from utils.metron import picture_to_power, picture_to_circle_parameters

ANALOG=0
DIGITAL=1

# Create your views here.

def index(request):
    num_readings = Reading.objects.all().count()
    num_users = User.objects.all().count()

    context = {
        'num_readings': num_readings,
        'num_users': num_users,
        'headers': request.META
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
            reading = form.save(commit=False)
            reading.user = request.user
            queryset=Settings.objects.filter(user=request.user.id)
            #### If settings haven't been created yet, set defaults (including calculating settings online)
            if queryset.count() == 0:
                old_settings,created = Settings.objects.update_or_create(user=request.user,
                                                                         defaults={'meter_type': ANALOG,
                                                                                   'x': 0,
                                                                                   'y': 0,
                                                                                   's': 0,
                                                                                   'h': 0,
                                                                                   'w': 0,
                                                                                   'r': 0,
                                                                                   'update': True, 
                                                                                   'calculate_online': True})
                old_settings.save()
            ####
            settings=queryset.first()
            if settings.update:
                if settings.calculate_online:
                    if settings.meter_type==ANALOG:
                        (settings.x,settings.y,settings.r)=picture_to_circle_parameters(reading.picture)
                    elif settings.meter_type==DIGITAL:
                        # ENE202: REPLACE THIS WITH parameter-finding algo 
                        (settings.x,settings.y,settings.s,settings.w,settings.h)=(0,0,1,1,1)
                settings.update=False
                settings.save()
            #reading.settings=settings
            if settings.calculate_online:
                if settings.meter_type==ANALOG:
                    numbers=picture_to_power(reading.picture,
                                             settings.x,
                                             settings.y,
                                             settings.r)
                elif settings.meter_type==DIGITAL:
                    # ENE202: REPLACE THIS WITH number-finding algo
                    numbers=(5,5,5,5,5)
                reading.firstNum=numbers[0]
                reading.secondNum=numbers[1]
                reading.thirdNum=numbers[2]
                reading.fourthNum=numbers[3]
                reading.fifthNum=numbers[4]
            if reading.time<datetime.datetime(2000,1,1):
                reading.time=datetime.datetime.now()

            reading.save()
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
                                                                     defaults={'meter_type': new_settings.meter_type,
                                                                               'x': new_settings.x,
                                                                               'y': new_settings.y,
                                                                               's': new_settings.s,
                                                                               'w': new_settings.w,
                                                                               'h': new_settings.h,
                                                                               'r': new_settings.r,
                                                                               'update': new_settings.update,
                                                                               'calculate_online': new_settings.calculate_online})
            old_settings.save()
            return HttpResponseRedirect('/')
    else:
        form = SettingsForm()
        queryset=Settings.objects.filter(user=request.user.id)
        if queryset.count() != 0:
            old_settings=queryset.first()
            form.fields['meter_type'].initial=old_settings.meter_type
            form.fields['x'].initial=old_settings.x
            form.fields['y'].initial=old_settings.y
            form.fields['r'].initial=old_settings.r
            form.fields['s'].initial=old_settings.s
            form.fields['w'].initial=old_settings.w
            form.fields['h'].initial=old_settings.h
            form.fields['update'].initial=old_settings.update
            form.fields['calculate_online'].initial=old_settings.calculate_online
        else:
            old_settings,created = Settings.objects.update_or_create(user=request.user,
                                                                     defaults={'meter_type': ANALOG,
                                                                               'x': 0,
                                                                               'y': 0,
                                                                               'r': 0,
                                                                               's': 0,
                                                                               'w': 0,
                                                                               'h': 0,
                                                                               'update': True, 
                                                                               'calculate_online': True})
            old_settings.save()

    context = {
        'form': form,
    }

    return render(request, 'change_settings.html', context)


from django.contrib.auth.mixins import LoginRequiredMixin

class SettingsView(LoginRequiredMixin, generic.ListView):
    model = Settings
    def get_queryset(self):
        return Settings.objects.filter(user=self.request.user)

def manual_settings(request):
    queryset=Reading.objects.filter(user=request.user.id)
    first_reading=queryset.first()
    pic_path=first_reading.picture.url
    queryset=Settings.objects.filter(user=request.user.id)
    settings=queryset.first()
    return render(request, 'manual_settings.html',{'meter_is_analog': settings.meter_type==ANALOG,
                                                   'pic_path': pic_path})

from readings.forms import ReadingSelectForm
def update_readings(request):
    #user_ob = get_user_model().objects.filter(id=user_id).first()
    #full_user_profile = UserProfile.objects.filter(user=user_ob).first()

    if request.method == 'POST':
        form = ReadingSelectForm(request.user.id,request.POST) #, user_id=request.user.id)
        if form.is_valid():
            queryset=Settings.objects.filter(user=request.user.id)
            settings=queryset.first()
            for reading in form.cleaned_data['readings']:
                if settings.update:
                    if settings.meter_type==ANALOG:
                        (settings.x,settings.y,settings.r)=picture_to_circle_parameters(reading.picture)
                    elif settings.meter_type==DIGITAL:
                        (settings.x, settings.y, settings.s, settings.w, settings.h)=(1,1,1,1,1)
                    settings.update=False
                    settings.save()
                #reading.settings=settings
                if settings.meter_type==ANALOG:
                    numbers=picture_to_power(reading.picture,
                                             settings.x,
                                             settings.y,
                                             settings.r)
                elif settings.meter_type==DIGITAL:
                    numbers=(6,6,6,6,6)
                reading.firstNum=numbers[0]
                reading.secondNum=numbers[1]
                reading.thirdNum=numbers[2]
                reading.fourthNum=numbers[3]
                reading.fifthNum=numbers[4]
                reading.save()
                
            return HttpResponseRedirect(reverse('reading_list')) #render(request, 'readings/reading_list.html')
    else:
        form = ReadingSelectForm(user=request.user.id)
        return render(request, 'update_readings.html', {'form' : form})
    
class ReadingView(LoginRequiredMixin, generic.ListView):
    model = Reading
    paginate_by=4
    
    def get_queryset(self):
        return Reading.objects.filter(user=self.request.user)
   
def csrf_failure(request, reason="tits"):
    context = {"headers": request.META} #{header: headers[header] for header in headers}
    return render(request, 'csrf.html', context)

