from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
import achivki
from achivki.main.views.forms import TaskCreationForm
from PIL import Image as PImage
from os.path import join as pjoin
import datetime

@login_required
def add_task(request):
    errors = [];
    if request.method == 'POST':
        form = TaskCreationForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save()
            task.user = User.objects.get(id=request.user.id)
            task.status = 0
            task.added = datetime.datetime.now()
            task.save()

            imfn = pjoin(achivki.settings_debug.MEDIA_ROOT, task.image.name)
            im = PImage.open(imfn)
            im.thumbnail((111,94), PImage.ANTIALIAS)
            im.save(imfn, "JPEG")
            return HttpResponseRedirect("/feed")
    else:
        form = TaskCreationForm()
    context = {
        'my_username' : request.user.username,
        'profile_name' : request.user.username,
        'gravatar_url' : request.user.get_profile().get_gravatar_url(),
        'is_authenticated' : True,
        'form': form,
    }
    return render_to_response("addtask.html", context)
