from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

@login_required()
def feed(request):
    context = {
        'my_username' : request.user.username,
        'profile_name' : request.user.username,
        'gravatar_url' : request.user.get_profile().get_gravatar_url(),
        'is_authenticated' : True,
        #TODO: add feed content, sidebar content
    }
    return render_to_response("feed.html", context)