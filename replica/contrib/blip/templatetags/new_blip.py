from django.template.loader import render_to_string
from django.template import Library
from django.template import RequestContext

from ..forms import BlipModelForm

register = Library()


@register.inclusion_tag('blip/templatetags/new_blip.html')
def new_blip(request):
	return {'form': BlipModelForm(),}

@register.simple_tag
def new_blip(request):
    return render_to_string('blip/templatetags/new_blip.html', {'form': BlipModelForm()}, context_instance=RequestContext(request))
