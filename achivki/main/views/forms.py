# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.utils.encoding import smart_unicode
from achivki.main.views.recaptcha.widgets import ReCaptcha
from recaptcha import captcha
from django.conf import settings

class ReCaptchaField(forms.CharField):
    default_error_messages = {
      'captcha_invalid': _(u'Вы неправильно ввели код с картинки')
    }
    def __init__(self, *args, **kwargs):
      self.widget = ReCaptcha
      self.required = True
      super(ReCaptchaField, self).__init__(*args, **kwargs)
    def clean(self, values):
      super(ReCaptchaField, self).clean(values[1])
      recaptcha_challenge_value = smart_unicode(values[0])
      recaptcha_response_value = smart_unicode(values[1])
      check_captcha = captcha.submit(recaptcha_challenge_value,
        recaptcha_response_value, settings.RECAPTCHA_PRIVATE_KEY, {})
      if not check_captcha.is_valid:
        raise forms.util.ValidationError(self.error_messages['captcha_invalid'])
      return values[0]


class MyUserCreationForm(UserCreationForm):
    email = forms.EmailField(label=_(u'E-mail'))
    username = forms.CharField(widget=forms.TextInput(attrs={'maxlength':75}),
                                label=_(u'Логин'))
    password1 = forms.CharField(widget=forms.PasswordInput(render_value=False),
                                label=_(u'Пароль'))
    password2 = forms.CharField(widget=forms.PasswordInput(render_value=False),
                                label=_(u'Подтвердите пароль'))
    recaptcha = ReCaptchaField(error_messages = {
            'required': u'Это поле должно быть заполнено',
            'invalid' : u'Указанное значение было неверно'
            },label=_(u'Введите код'))


