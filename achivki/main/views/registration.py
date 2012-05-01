# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib import auth
from django.core.context_processors import csrf
from achivki.main.views.forms import MyUserCreationForm
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from achivki.main.models import UProfile


def register(request):
    errors = [];
    if request.method == 'POST':
        #form = UserCreationForm(request.POST)
        form = MyUserCreationForm(request.POST)
        if (form.is_valid()):
            user_email = request.POST.get('email','')
            is_email = UProfile.objects.filter(email=user_email)
            if is_email:
                errors.append( _(u'Пользователь с таким Email уже существует'))
            else:
                new_user = form.save(request)
                new_profile = UProfile(id=new_user.id, name=request.POST['username'], email=user_email,
                                          password = request.POST['password1'])
                new_profile.save()
                user = auth.authenticate(username=request.POST['username'],
                                        password=request.POST['password1'])
                auth.login(request, user)
                return HttpResponseRedirect("/base")
    else:
        form = MyUserCreationForm()
        #form = UserCreationForm()
    context = {
        'form': form,
        'errors': errors
    }
    context.update(csrf(request))
    return render_to_response("register.html", context)

def losepassword(request):
    errors = []
    success = 0
    if request.method == 'POST':
        if(request.POST['email']):
            user_email = request.POST.get('email','')
            p = UProfile.objects.filter(email=user_email)
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


