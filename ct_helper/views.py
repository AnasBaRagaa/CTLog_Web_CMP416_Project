from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, redirect
from django.views import generic

from ct_helper.forms import UserForm

def index(request):
    return render(request,template_name='ct_helper/index.html')
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
    template_name = 'ct_helper/update.html'  # Generic template

    def get_object(self, queryset=None):
        obj = super(BaseUpdateView, self).get_object()
        if obj.owner != self.request.user:
            raise Http404  # prevent users from accessing records they do not own
        return obj

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super(BaseUpdateView, self).form_valid(form)


class BaseCreateView(LoginRequiredMixin, generic.CreateView):
    success_message = "Record was added successfully."
    template_name = 'ct_helper/update.html'  # Generic template
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
