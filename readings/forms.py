from django import forms
from readings.models import Reading
    
class UserRegistrationForm(forms.Form):
    username = forms.CharField(help_text="A unique username")
    password = forms.CharField(help_text="Password")
    email = forms.CharField(help_text="Email")

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Reading
        fields = ['time','firstNum', 'secondNum','thirdNum','fourthNum','fifthNum']
        # widgets = {
        #     'time': forms.DateTimeInput,
        # }
