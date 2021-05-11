# Anas Ba Ragaa _ b00075797
from datetime import datetime

from django import forms
from django.forms import ModelChoiceField, DateInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Hospital, Patient, Surgeon, Drug, Prescription, Test, Operation


class UserForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2',)

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        if commit:
            user.save()
        return user


class BaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        if 'user' in kwargs.keys():
            user = kwargs.pop('user')
            self.user = user
        else:
            self.user = None
        super(BaseForm, self).__init__(*args, **kwargs)


class SurgeonForm(BaseForm):
    class Meta:
        model = Surgeon
        exclude = ['owner']


class HospitalForm(BaseForm):
    class Meta:
        model = Hospital
        exclude = ['owner']


class PatientForm(BaseForm):
    def __init__(self, *args, **kwargs):
        super(PatientForm, self).__init__(*args, **kwargs)
        self.fields['hospital'] = ModelChoiceField(queryset=Hospital.objects.filter(owner=self.user))
       # self.fields['patient_date_of_birth']= forms.DateField(widget=DateInput(attrs={'max': datetime.now().strftime("%Y-%m-%d"), 'type':'date'}))
    class Meta:
        model = Patient
        exclude = ['owner']
        widgets = {
           'patient_date_of_birth': DateInput(attrs={'max': datetime.now().strftime("%Y-%m-%d"), 'type':'date'})

        }
