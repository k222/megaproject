import os, sys, traceback

sys.path.append("/home/esgv/public_html/");
os.environ['DJANGO_SETTINGS_MODULE'] = 'achivki.settings'
os.environ['PYTHON_EGG_CACHE'] = '/home/esgv/.python_cache'

import django.core.handlers.wsgi
_application = django.core.handlers.wsgi.WSGIHandler()

class EmptyApplicationResponse(Exception):
    pass

def application(environ, start_response):
    try:
        lines = list(_application(environ, start_response))

        if not lines:
            raise EmptyApplicationResponse()

        return lines

    except Exception as e:
        trace = traceback.format_exc()
        output = trace

        response_headers = [
            ('Content-type', 'text/plain'),
            ('Content-Length', str(len(output)))
        ]
        start_response('500 Internal Server Error', response_headers)
        return [output]
