# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.utils.translation import ugettext_lazy as _
from django.core.validators import email_re

@login_required
def settings(request):
    errors = []
    message = ""
    if request.method == 'POST':
        change_kind = request.POST['change_kind']
        if change_kind == 'apply_all':
            old_password = request.POST['oldpassword']
            password1 = request.POST['newpassword1']
            password2 = request.POST['newpassword2']
			if not (password1 == "" and password2 == ""):
				if password1 != password2:
					errors.append(_(u'Введённые пароли не совпадают.'))
				else:
					if len(password1) < 6:
						errors.append(_(u'Новый пароль должен содержать не менее 6-ти символов.'))
					else:
						if request.user.check_password(old_password):
							request.user.set_password(password1)
							request.user.save()
							message = _(u"Пароль изменён успешно.")
						else:
							errors.append(_(u'Старый пароль введён неверно.'))
        
            email1 = request.POST['new_email']
            email2 = request.POST['confirm_email']
			if not (email1 == "" and email2 == ""):
                if email1 != email2:
                    errors.append(_(u"Введённые адреса электронной почты не совпадают."))
                else:
                    try:
                        User.objects.get(email=email1)
                        errors.append(_(u"Указанный e-mail уже используется."))
                    except User.DoesNotExist:
                        if email_re.match(email1):
                            request.user.email = email1;
                            request.user.save();
                            message = _(u"E-mail изменён успешно.")
                        else:
                            errors.append(_(u'Указан неверный e-mail.'))



    context = {
        'is_authenticated' : True,
        'profile_name' : request.user.username,
        'gravatar_url' : request.user.get_profile().get_gravatar_url(),
        'errors': errors,
        'message': message,
        'email': request.user.email,
    }
    return render_to_response("settings.html", context)
