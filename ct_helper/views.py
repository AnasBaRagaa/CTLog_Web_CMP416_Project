from django.shortcuts import render

def index(request):
    context = {'contacts_list': contact_list}
    return render(request, 'phonebook/base.html', context)