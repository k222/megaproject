# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class MyUserCreationForm(UserCreationForm):
    email = forms.EmailField(label=_(u'E-mail'))
    username = forms.CharField(widget=forms.TextInput(attrs={'maxlength':75}),
                                label=_(u'Логин'))
    password1 = forms.CharField(widget=forms.PasswordInput(render_value=False),
                                label=_(u'Пароль'))
    password2 = forms.CharField(widget=forms.PasswordInput(render_value=False),
                                label=_(u'Подтвердите пароль'))

