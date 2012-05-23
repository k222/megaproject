# -*- coding: utf-8 -*-
import email
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.utils.encoding import smart_unicode
from achivki.main.models import UserProfile, Task
from achivki.main.views.recaptcha.widgets import ReCaptcha
from recaptcha import captcha
from django.conf import settings
from achivki.bootstrap_forms.forms import BootstrapModelForm, Fieldset
from django.contrib.admin import widgets

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

class RegistrationForm(BootstrapModelForm):
    class Meta:
        model = User
        fields = ("username",)

    email = forms.EmailField(label=_(u'E-mail'), required=True,
            help_text = _(u'Введите действующий адрес электронной почты.'),)

    recaptcha = ReCaptchaField(error_messages = {
            'required': u'Это поле должно быть заполнено',
            'invalid' : u'Указанное значение было неверно'
            },label=_(u'Введите код подтверждения'), required=True)

    error_messages = {
        'duplicate_username': _(u'Пользователь с таким именем уже существует'),
        'password_mismatch': _(u'Пароль и подтверждение должны совпадать.'),
        'duplicate_email': _(u'Указанные email уже используется'),
    }

    username = forms.RegexField(label=_(u'Имя пользователя'), max_length=30,
        regex=r'^[\w.@+-]+$',
        help_text = _(u'Обязательное поле. Не более 30 символов A-Z, a-z, 0-9 и @ . + - _'),
        error_messages = {
            'invalid': _(u'Это поле может содержать только символы A-Z, a-z, 0-9 и @ . + - _')},
        required=True)

    password1 = forms.CharField(label=_(u'Пароль'),
        widget=forms.PasswordInput, required=True)

    password2 = forms.CharField(label=_(u'Подтверждение пароля'),
        widget=forms.PasswordInput,
        help_text = _(u'Введите такой же пароль, как и выше, для подтверждения.'),
        required=True)

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(self.error_messages['password_mismatch'])
        return password2

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(self.error_messages['duplicate_email'])

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
########################################################################################################################

class TaskCreationForm(BootstrapModelForm):
    class Meta:
        model = Task
        exclude = ("user", "status", "added")

    name = forms.CharField(label=_(u"Название задания:"),
        help_text=_(u"Введите сюда название создаваемого задания. Не более 100 символов. Обязательно для заполнения."),
        required=True, max_length=100)
    description = forms.CharField(widget=forms.widgets.Textarea(attrs={ 'rows':5 }),
        label=_(u"Описание задания:"),
        help_text=_(u"Введите сюда название создаваемого задания. Не более 500 символов. Обязательно для заполнения."),
        max_length=500)
    image = forms.ImageField(label=_(u"Иллюстрация:"),
        help_text=_(u"Добавьте иллюстрацию для задания."), required=False)
    #time = forms.DateTimeField(widget=widgets.AdminSplitDateTime(), label=_(u"Время выполнения:"),
    #    help_text=_(u"Укажите время выполнения задания."), )

    #tags = forms.CharField(label=_(u"Тэги задания:"),
    #    help_text=_(u"Перечисляются через точку с запятой."), max_length=200)

    def save(self, commit=False):
        Task =  super(TaskCreationForm, self).save(commit=False)
        if commit:
            Task.save()
        return Task