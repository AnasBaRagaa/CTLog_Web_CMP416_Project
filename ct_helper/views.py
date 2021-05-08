from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

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


def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            u = authenticate(request, username=username, password=password)
            if u is not None:
                login(request, u)
                messages.info(request, 'Logged in as {}'.format(username))
                return redirect('ct_helper:index')
            else:
                messages.error(request, "Wrong username or password.")
        else:
            messages.error(request, "Wrong username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name='registration/login.html', context={'form': form})
