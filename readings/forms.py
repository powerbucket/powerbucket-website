from django import forms
from readings.models import Reading, Settings


class UserRegistrationForm(forms.Form):
    username = forms.CharField(help_text="A unique username")
    password = forms.CharField(help_text="Password")
    email = forms.CharField(help_text="Email")

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Reading
        fields = ['time','firstNum', 'secondNum','thirdNum','fourthNum','fifthNum', 'picture']
        # widgets = {
        #     'time': forms.DateTimeInput,
        # }

class SettingsForm(forms.ModelForm):
    class Meta:
        model = Settings
        fields = ['x', 'y', 'r', 'update']

class ReadingSelectForm(forms.Form):
    class Meta:
        model=Reading
        
    def __init__(self,user,*args,**kwargs):
        super(ReadingSelectForm, self).__init__(*args, **kwargs)
        self.fields['readings'] = forms.ModelMultipleChoiceField(queryset=Reading.objects.filter(user=user),
                                                     widget=forms.CheckboxSelectMultiple)
