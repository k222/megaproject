import os, sys 

sys.path.append("/home/esgv/public_html/");
os.environ['DJANGO_SETTINGS_MODULE'] = 'achivki.settings'
os.environ['PYTHON_EGG_CACHE'] = '/home/esgv/.python_cache'

import django.core.handlers.wsgi
_application = django.core.handlers.wsgi.WSGIHandler()

def application(environ, start_response):
    #environ['PATH_INFO'] = environ['SCRIPT_NAME'] + environ['PATH_INFO']
    try:
        lines = list(_application(environ, start_response))
        if lines:
            return lines
        else:
            start_response('200 OK', [('Content-Type', 'text/plain')])
            return ['Stupid empty application!']
        
    except Exception as e:
        start_response('200 OK', [('Content-Type', 'text/plain')])
        return ['Exception, sir! {0}'.format(e)]