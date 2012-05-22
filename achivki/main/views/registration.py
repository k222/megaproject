# -*- coding: utf-8 -*-
from smtplib import SMTPException
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib import auth
from django.core.context_processors import csrf
from achivki.main.views.forms import RegistrationForm
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import UserManager, User


def register(request):
    if not request.user.is_anonymous():
        return HttpResponseRedirect('/feed')
    errors = [];
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save(request)
            request.user = auth.authenticate(username=request.POST['username'],
                                             password=request.POST['password1'])
            auth.login(request, request.user)
            return HttpResponseRedirect("/feed")
    else:
        form = RegistrationForm()
    return render_to_response("register.html", {'form' : form})

def lost_password(request):
    if not request.user.is_anonymous():
        return HttpResponseRedirect('/feed')

    errors = []
    success = 0
    if request.method == 'POST':
        if(request.POST['email']):
            user_email = request.POST.get('email','')
            try:
                user = User.objects.get(email=user_email)
            except User.DoesNotExist:
                errors.append(_(u"Пользователь с Email:%s не найден" % user_email ))
            else:
                new_password = User.objects.make_random_password()
                user.set_password(new_password)
                msg = _(u" Your login: %(name)s     Your password: %(password)s" % {'name':user.username, 'password':new_password})
                topic = _(u"Lost password TickIt")
                try:
                    send_mail(topic, msg, 'tickit@bk.ru', [user_email])
                    user.save()
                except SMTPException:
                    errors.append(_(u"Не удаётся отправить письмо с новым паролем. Пожалуйста, попробуйте позже."))
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
    return render_to_response("lost_password.html", context)


