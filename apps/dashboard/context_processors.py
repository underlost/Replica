from django.conf import settings


def template_settings(request):
    return {'site_name': settings.SITE_NAME,}

def baseurl(request):
    #Return a BASE_URL template context for the current request.
    return {'BASE_URL': 'http://' + request.get_host(),}