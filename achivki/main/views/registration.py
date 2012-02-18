from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib import auth
from django.core.context_processors import csrf
from achivki.main.views.forms import myUserCreationForm

def register(request):
    if request.method == 'POST':
        #form = UserCreationForm(request.POST)
        form = myUserCreationForm(request.POST)
        if (form.is_valid()):
            new_user = form.save(request)

            user = auth.authenticate(username=request.POST['username'], password=request.POST['password1'])
            auth.login(request, user)
            return HttpResponseRedirect("/base")
    else:
        form = myUserCreationForm()
        #form = UserCreationForm()
    context = {
        'form': form
    }
    context.update(csrf(request))
    return render_to_response("registration.html", context)

