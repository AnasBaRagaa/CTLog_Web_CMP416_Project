# Anas Ba Ragaa _ b00075797
from datetime import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelChoiceField, DateInput, CharField
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
            'patient_date_of_birth': DateInput(attrs={'max': datetime.now().strftime("%Y-%m-%d"), 'type': 'date'})

        }


class OperationForm(BaseForm):
    def __init__(self, *args, **kwargs):
        update = False
        if 'update' in kwargs.keys():
            update = kwargs.pop('update')

        super(OperationForm, self).__init__(*args, **kwargs)
        self.fields['surgeon'] = ModelChoiceField(queryset=Surgeon.objects.filter(owner=self.user))
        if not update:
            self.fields['patient'] = ModelChoiceField(queryset=Patient.objects.filter(owner=self.user))
        else:
            self.fields['patient'] = ModelChoiceField(queryset=Patient.objects.filter(owner=self.user),disabled=True)

    class Meta:
        model = Operation
        exclude = ['hospital', 'owner']
        widgets = {
            'admission_date': DateInput(attrs={'type': 'date'}),
            'operation_date': DateInput(attrs={'type': 'date'}),
            'discharge_date': DateInput(attrs={'type': 'date'}),

        }

    def clean(self):
        form_data = self.cleaned_data
        if form_data['admission_date'] > form_data['operation_date']:
            self._errors['admission'] = ['admission date cannot be after operation date']
        if form_data['admission_date'] > form_data['discharge_date']:
            self._errors['admission'] = ['admission date cannot be after discharge date']
        if form_data['operation_date'] > form_data['discharge_date']:
            self._errors['operation_date'] = ['operation date cannot be after discharge date']
        if form_data['patient'].patient_date_of_birth > form_data['admission_date']:
            self._errors['admission_date'] = ['admission date cannot be before patient DOB']


class DrugForm(BaseForm):
    class Meta:
        model = Drug
        exclude = ['owner']
