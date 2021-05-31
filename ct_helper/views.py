from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from ct_helper.forms import UserForm, HospitalForm, SurgeonForm, PatientForm, DrugForm, OperationForm, TestForm, \
    PrescriptionForm
from .models import Hospital, Patient, Surgeon, Drug, Prescription, Test, Operation


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
    extra_context = {'filter_param': False}

    # filter based on the current user
    def get_queryset(self, *args, **kwargs):
        qs = super(BaseListView, self).get_queryset(*args, **kwargs)
        qs = qs.filter(owner=self.request.user)
        return qs


class BaseDetailView(LoginRequiredMixin, generic.DetailView):
    context_object_name = "object"

    def get_object(self, queryset=None):
        obj = super(BaseDetailView, self).get_object()
        if obj.owner != self.request.user:
            raise Http404(
                'You do not have permission to access this record')  # prevent users from deleting records they do not own
        return obj


class BaseDeleteView(LoginRequiredMixin, generic.DeleteView):
    success_message = "Record was deleted successfully."
    template_name = 'ct_helper/delete.html'  # Generic template

    def get_object(self, queryset=None):
        obj = super(BaseDeleteView, self).get_object()
        if obj.owner != self.request.user:
            # prevent users from deleting records they do not own
            raise Http404('You do not have permission to access this record')
        return obj

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(BaseDeleteView, self).delete(request, *args, **kwargs)

    def get_success_url(self):
        if self.request.GET.get('next', '') != '':
            # redirect back to the next page if this request was redirected from another page and has a next parameter
            self.request.session['data'] = self.request.POST
            return self.request.GET.get('next', '')
        return super(BaseDeleteView, self).get_success_url()


class BaseUpdateView(LoginRequiredMixin, generic.UpdateView):
    success_message = "Record was updated successfully."
    template_name = 'ct_helper/update.html'  # Generic template for insert and update

    def get_object(self, queryset=None):
        obj = super(BaseUpdateView, self).get_object()
        if obj.owner != self.request.user:
            raise Http404(
                'You do not have permission to access this record')  # prevent users from accessing records they do not own
        return obj

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super(BaseUpdateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(BaseUpdateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_success_url(self):
        if self.request.GET.get('next', '') != '':
            # redirect back to the next page if this request was redirected from another page and has a next parameter
            self.request.session['data'] = self.request.POST
            return self.request.GET.get('next', '')
        return super(BaseUpdateView, self).get_success_url()


class BaseCreateView(LoginRequiredMixin, generic.CreateView):
    success_message = "Record was added successfully."
    template_name = 'ct_helper/update.html'  # Generic template for insert and update

    # def get_form(self, form_class=None):

    def get_success_url(self):
        if self.request.GET.get('next', '') != '':
            # redirect back to the next page if this request was redirected from another page and has a next parameter
            self.request.session['data'] = self.request.POST
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


# Index----------------------------------------


class IndexView(BaseListView):
    template_name = 'ct_helper/index.html'
    model = Patient


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

    def get_queryset(self, *args, **kwargs):
        qs = super(BaseListView, self).get_queryset(*args, **kwargs)
        name = self.request.GET.get('name', '')
        if (name != ''):
            qs = qs.filter(patient_name__contains=name)
            self.extra_context['filter_param'] = name
        else:
            self.extra_context['filter_param'] = False
        return qs


class PatientDeleteView(BaseDeleteView):
    model = Patient
    success_message = "Patient was deleted successfully"
    success_url = reverse_lazy('ct_helper:patients')


##
#
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

    def get_queryset(self, *args, **kwargs):
        qs = super(SurgeonListView, self).get_queryset(*args, **kwargs)
        name = self.request.GET.get('name', '')
        if (name != ''):
            qs = qs.filter(surgeon_name__contains=name)
            self.extra_context['filter_param'] = name
        else:
            self.extra_context['filter_param'] = False
        return qs


class SurgeonDeleteView(BaseDeleteView):
    model = Surgeon
    success_message = "Surgeon was deleted successfully"
    success_url = reverse_lazy('ct_helper:surgeons')


# ------------------------------------------------------------
# Operation views:


class OperationCreateView(BaseCreateView):
    model = Operation
    success_message = 'New operation added successfully'
    success_url = reverse_lazy('ct_helper:operations')
    form_class = OperationForm
    template_name = "ct_helper/operation/update.html"

    def form_valid(self, form):
        form.instance.hospital = form.instance.patient.hospital
        return super(OperationCreateView, self).form_valid(form)


class OperationUpdateView(BaseUpdateView):
    model = Operation
    success_message = 'Operation updated successfully'
    success_url = reverse_lazy('ct_helper:operations')
    form_class = OperationForm
    template_name = "ct_helper/operation/update.html"

    def get_form_kwargs(self):
        kwargs = super(OperationUpdateView, self).get_form_kwargs()
        kwargs.update({'update': True})
        return kwargs


class OperationListView(BaseListView):
    model = Operation
    template_name = "ct_helper/operation/list.html"
    extra_context = {'filter_param': False, 'filter_type': False}
    def get_queryset(self, *args, **kwargs):
        qs = super(OperationListView, self).get_queryset(*args, **kwargs)
        name = self.request.GET.get('name', '')
        search_by = self.request.GET.get('search_by', '')
        if (name != ''):
            if search_by == 'patient':
                qs = qs.filter(patient__patient_name__contains=name)

            else:
                qs = qs.filter(surgeon__surgeon_name__contains=name)

            self.extra_context['filter_param'] = name
            self.extra_context['filter_type'] = search_by
        else:
            self.extra_context['filter_param'] = False
            self.extra_context['filter_type'] = False
        return qs

class OperationDeleteView(BaseDeleteView):
    model = Operation
    success_message = "Operation was deleted successfully"
    success_url = reverse_lazy('ct_helper:operations')


class OperationDetailView(BaseDetailView):
    model = Operation
    context_object_name = "op"
    template_name = "ct_helper/operation/detail.html"





# -----------------------------------------------------------
# Drug views:
class DrugCreateView(BaseCreateView):
    model = Drug
    success_message = 'New drug added successfully'
    success_url = reverse_lazy('ct_helper:drugs')
    form_class = DrugForm


class DrugUpdateView(BaseUpdateView):
    model = Drug
    success_message = 'Drug updated successfully'
    success_url = reverse_lazy('ct_helper:drugs')
    form_class = DrugForm


class DrugListView(BaseListView):
    model = Drug
    template_name = "ct_helper/drug/list.html"

    def get_queryset(self, *args, **kwargs):
        qs = super(BaseListView, self).get_queryset(*args, **kwargs)
        name = self.request.GET.get('name', '')
        if (name != ''):
            qs = qs.filter(drug_name__contains=name)
            self.extra_context['filter_param'] = name
        else:
            self.extra_context['filter_param'] = False
        return qs


class DrugDeleteView(BaseDeleteView):
    model = Drug
    success_message = "Drug was deleted successfully"
    success_url = reverse_lazy('ct_helper:drugs')


# -------------------------------------------------------------
# Test views:
class TestCreateView(BaseCreateView):
    model = Test
    success_message = 'New tests added successfully'
    success_url = reverse_lazy('ct_helper:operations')
    form_class = TestForm

    def form_valid(self, form):
        form.instance.operation = Operation.objects.get(pk=self.kwargs['operation'])
        form.instance.order = self.kwargs['order']
        return super(TestCreateView, self).form_valid(form)


class TestUpdateView(BaseUpdateView):
    model = Test
    success_message = 'Tests updated successfully'
    success_url = reverse_lazy('ct_helper:operations')
    form_class = TestForm


class TestDeleteView(BaseDeleteView):
    model = Test
    success_message = "Tests was deleted successfully"
    success_url = reverse_lazy('ct_helper:operations')


# ------------------------------------------------------------------------
# Prescription views:
class PrescriptionCreateView(BaseCreateView):
    model = Prescription
    success_message = 'New prescription added successfully'
    success_url = reverse_lazy('ct_helper:operations')
    form_class = PrescriptionForm
    template_name = 'ct_helper/prescription/update.html'

    def form_valid(self, form):
        form.instance.operation = Operation.objects.get(pk=self.kwargs['operation'])
        return super(PrescriptionCreateView, self).form_valid(form)


class PrescriptionUpdateView(BaseUpdateView):
    model = Prescription
    success_message = 'Prescription updated successfully'
    success_url = reverse_lazy('ct_helper:operations')
    form_class = PrescriptionForm
    template_name = 'ct_helper/prescription/update.html'


class PrescriptionDeleteView(BaseDeleteView):
    model = Prescription
    success_message = "Prescription was deleted successfully"
    success_url = reverse_lazy('ct_helper:operations')
