from django.db import models
from django.contrib.auth.models import User

from datetime import datetime

from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Reading(models.Model):

    time=models.DateTimeField(help_text="Time at which reading was taken (date-time)", default=datetime.now, primary_key=True)
    firstNum = models.FloatField()
    secondNum = models.FloatField()
    thirdNum = models.FloatField()
    fourthNum = models.FloatField()
    fifthNum = models.FloatField()
    picture = models.ImageField(null=True,blank=True)
    #settings = models.ForeignKey(Settings, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-time']

    def get_absolute_url(self):
        return reverse('reading', args=[str(self.id)])
        
    def __str__(self):
        return str(self.time)

class Settings(models.Model):
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    r = models.IntegerField(default=0)
    s = models.IntegerField(default=0)
    w = models.IntegerField(default=0)
    h = models.IntegerField(default=0)
    ANALOG=0
    DIGITAL=1
    METER_TYPE_CHOICES=[
        (ANALOG, 'Analog'),
        (DIGITAL, 'Digital'),
    ]
    meter_type = models.IntegerField(choices=METER_TYPE_CHOICES,
                                     default=ANALOG)
    update = models.BooleanField(default=True)
    calculate_online = models.BooleanField(default=True)
    user = models.OneToOneField(User,
                                on_delete=models.SET_NULL,
                                null=True)

# @receiver(post_save, sender=User)
# def create_user_settings(sender, instance, created, **kwargs):
#     if created:
#         Settings.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_settings(sender, instance, **kwargs):
#     instance.settings.save()
