# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib import auth
from django.core.context_processors import csrf
from achivki.main.views.forms import MyUserCreationForm
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User



def register(request):
    error="";
    if request.method == 'POST':
        #form = UserCreationForm(request.POST)
        form = MyUserCreationForm(request.POST)
        if (form.is_valid()):
            new_user = form.save(request)
            user = auth.authenticate(username=request.POST['username'],
                                        password=request.POST['password1'])
            auth.login(request, user)
            return HttpResponseRedirect("/base")
    else:
        form = MyUserCreationForm()
        #form = UserCreationForm()
    context = {
        'form': form,
        'error': error
    }
    context.update(csrf(request))
    return render_to_response("register.html", context)

def losepassword(request):
    errors = []
    success = 0
    if request.method == 'POST':
        if(request.POST['email']):
            user_email = request.POST.get('email','')
            print user_email
            p = User.objects.filter(email=user_email)
            if p:
                msg = _(u" Ваш логин: %s <br> Ваш пароль: %s" % p.username, p.password)
                topic = _(u"Lost password achivki.ru")
                send_mail(topic, msg, 'Ann1137@ya.ru',
                    [user_email], fail_silently=False)
            else:
                errors.append(_(u"Пользователь с Email:%s не найден" % user_email ))
        else:
            errors.append(_(u"Не заполнено поле Email"))
        if(not errors):
            success=1;
    context = {
        'errors': errors,
        'success':success,
        'email':request.POST.get('email', '')
        }
    context.update(csrf(request))
    return render_to_response("losepassword.html", context)


