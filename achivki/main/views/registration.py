# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib import auth
from django.core.context_processors import csrf
from achivki.main.views.forms import MyUserCreationForm
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from achivki.main.models import UserProfile


def register(request):
    errors = [];
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            form.save(request)
            request.user = auth.authenticate(username=request.POST['username'],
                                             password=request.POST['password1'])
            auth.login(request, request.user)
            return HttpResponseRedirect("/feed")
    else:
        form = MyUserCreationForm()
    return render_to_response("register.html", {'form' : form})

def losepassword(request):
    errors = []
    success = 0
    if request.method == 'POST':
        if(request.POST['email']):
            user_email = request.POST.get('email','')
            p = UserProfile.objects.filter(email=user_email)
            if p:
                msg = _(u" Your login: %(name)s <br> Your password: %(password)s" % {'name':p[0].name, 'password':p[0].password})
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


