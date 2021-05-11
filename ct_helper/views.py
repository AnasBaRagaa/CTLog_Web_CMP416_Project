from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from ct_helper.forms import UserForm, HospitalForm, SurgeonForm, PatientForm
from .models import Hospital, Patient, Surgeon, Drug, Prescription, Test, Operation


def index(request):
    return render(request, template_name='ct_helper/index.html')


def profile(request):
    return redirect('ct_helper:index')


def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request=request, user=user)
            messages.success(request, 'Successful registration')
            return redirect('ct_helper:index')
        messages.error(request, 'Unsuccessful registration')
    form = UserForm
    return render(request, template_name="registration/register.html", context={'form': form})


def logout_user(request):
    logout(request)
    messages.info(request, "User logged out")
    return redirect('ct_helper:index')


# Subclassing the generic classes to include ownership check and assignment of the records and enforce login

class BaseListView(LoginRequiredMixin, generic.ListView):
    context_object_name = 'objects'

    # filter based on the current user
    def get_queryset(self, *args, **kwargs):
        qs = super(BaseListView, self).get_queryset(*args, **kwargs)
        qs = qs.filter(owner=self.request.user)
        return qs


class BaseDetailView(LoginRequiredMixin, generic.DetailView):
    def get_object(self, queryset=None):
        obj = super(BaseDeleteView, self).get_object()
        if obj.owner != self.request.user:
            raise Http404  # prevent users from deleting records they do not own
        return obj


class BaseDeleteView(LoginRequiredMixin, generic.DeleteView):
    success_message = "Record was deleted successfully."
    template_name = 'ct_helper/delete.html'  # Generic template

    def get_object(self, queryset=None):
        obj = super(BaseDeleteView, self).get_object()
        if obj.owner != self.request.user:
            raise Http404  # prevent users from deleting records they do not own
        return obj

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(BaseDeleteView, self).delete(request, *args, **kwargs)


class BaseUpdateView(LoginRequiredMixin, generic.UpdateView):
    success_message = "Record was updated successfully."
    template_name = 'ct_helper/update.html'  # Generic template for insert and update

    def get_object(self, queryset=None):
        obj = super(BaseUpdateView, self).get_object()
        if obj.owner != self.request.user:
            raise Http404  # prevent users from accessing records they do not own
        return obj

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super(BaseUpdateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(BaseUpdateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class BaseCreateView(LoginRequiredMixin, generic.CreateView):
    success_message = "Record was added successfully."
    template_name = 'ct_helper/update.html'  # Generic template for insert and update

    def get_success_url(self):
        if (self.request.GET.get('next', '') != ''):
            # redirect back to the next page if this request was redirected from another page and has a next parameter
            return self.request.GET.get('next', '')
        return super(BaseCreateView, self).get_success_url()

    # send  current user to the form
    def get_form_kwargs(self):
        kwargs = super(BaseCreateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    # save the current user as the owner of the created record
    def form_valid(self, form):
        user = self.request.user
        form.instance.owner = user
        messages.success(self.request, self.success_message)
        return super(BaseCreateView, self).form_valid(form)


# Hospital views:
class HospitalCreateView(BaseCreateView):
    model = Hospital
    success_message = 'New hospital added successfully'
    success_url = reverse_lazy('ct_helper:hospitals')
    form_class = HospitalForm


class HospitalUpdateView(BaseUpdateView):
    model = Hospital
    success_message = 'Hospital was updated successfully'
    success_url = reverse_lazy('ct_helper:hospitals')
    form_class = HospitalForm


class HospitalListView(BaseListView):
    model = Hospital
    template_name = "ct_helper/hospital/list.html"


class HospitalDeleteView(BaseDeleteView):
    model = Hospital
    success_message = "Hospital was deleted successfully"
    success_url = reverse_lazy('ct_helper:hospitals')


# ---------------------------------------------------
# Patient views:
class PatientCreateView(BaseCreateView):
    model = Patient
    success_message = 'New patient added successfully'
    success_url = reverse_lazy('ct_helper:patients')
    form_class = PatientForm
    template_name = 'ct_helper/patient/update.html'


class PatientUpdateView(BaseUpdateView):
    model = Patient
    success_message = 'Patient updated successfully'
    success_url = reverse_lazy('ct_helper:patients')
    form_class = PatientForm
    template_name = 'ct_helper/patient/update.html'


class PatientListView(BaseListView):
    model = Patient
    template_name = "ct_helper/patient/list.html"


class PatientDeleteView(BaseDeleteView):
    model = Patient
    success_message = "Patient was deleted successfully"
    success_url = reverse_lazy('ct_helper:patients')


# ------------------------------------------------------
# Surgeon views:
class SurgeonCreateView(BaseCreateView):
    model = Surgeon
    success_message = 'New surgeon added successfully'
    success_url = reverse_lazy('ct_helper:surgeons')
    form_class = SurgeonForm


class SurgeonUpdateView(BaseUpdateView):
    model = Surgeon
    success_message = 'Surgeon updated successfully'
    success_url = reverse_lazy('ct_helper:surgeons')
    form_class = SurgeonForm


class SurgeonListView(BaseListView):
    model = Surgeon
    template_name = "ct_helper/surgeon/list.html"


class SurgeonDeleteView(BaseDeleteView):
    model = Surgeon
    success_message = "Surgeon was deleted successfully"
    success_url = reverse_lazy('ct_helper:surgeons')

# ------------------------------------------------------------
# Operation views:

# -----------------------------------------------------------
# Drug views:

# -------------------------------------------------------------
# Test views:

# ------------------------------------------------------------------------
# Prescription views:
