from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.

class Reading(models.Model):

    time=models.DateTimeField(help_text="Time at which reading was taken (date-time)", default=datetime.now, primary_key=True)
    firstNum = models.FloatField()
    secondNum = models.FloatField()
    thirdNum = models.FloatField()
    fourthNum = models.FloatField()
    fifthNum = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-time']

    def get_absolute_url(self):
        return reverse('reading', args=[str(self.id)])
        
    def __str__(self):
        return self.time

