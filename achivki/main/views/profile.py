from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import  render_to_response

@login_required()
def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404

    is_my_page = (user.username == request.user.username)

    context = {
        'is_my_page' : is_my_page,
        'is_authenticated' : True,
        'user_is_authenticated' : user.is_authenticated(),
        'profile_name' : user.username,
        'my_username' : request.user.username,
        'gravatar_url' : user.get_profile().get_gravatar_url()
        #TODO: add feed content
    }

    return render_to_response("profile.html", context)