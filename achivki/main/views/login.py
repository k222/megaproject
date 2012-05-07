from django.http import HttpResponseRedirect
from django.contrib.auth.views import login
def mylogin(request, redirect='/feed'):
    if request.user.is_authenticated():
        return HttpResponseRedirect(redirect)
    else:
        return login(request, template_name='login.html')
