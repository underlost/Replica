from django.conf import settings


def template_settings(request):
    return {
        'site_name': settings.SITE_NAME,
        'site_desc': settings.SITE_DESC,
        'site_url': settings.SITE_URL,
        'site_register': settings.ALLOW_NEW_REGISTRATIONS,
        'BASE_URL': 'http://' + request.get_host(),
        'BASE_HOST': request.get_host().split(':')[0],
    }

def base_url(request):
    #Return a BASE_URL template context for the current request.
    return {'BASE_URL': 'http://' + request.get_host(),}

def base_host(request):
    #Return a BASE_HOST template context for the current request.
    return {'BASE_HOST': request.get_host().split(':')[0],}
