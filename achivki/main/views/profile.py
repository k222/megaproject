from django.http import Http404
from achivki.main.models import UProfile



def profile(request, id):
    try:
        prof = UProfile.objects.get(pk=id)

    except UProfile.DoesNotExist:
        raise Http404

    context = {
        'authenticated' : prof.is_authenticated()

    }