from __future__ import absolute_import
from urlparse import urlparse

from django import template
from ..models import Entry

register = template.Library()

@register.inclusion_tag('replica/templatetags/render_latest.html')
def render_latest(num):
	objects = Entry.objects.published()[:num]
	return {
		'objects': objects,
	}
	
@register.inclusion_tag('replica/templatetags/render_latest_entries.html')
def render_latest_entries(num):
	objects = Entry.objects.all()[:num]
	return {
		'objects': objects,
	}   

@register.inclusion_tag('replica/templatetags/month_links_snippet.html')
def render_month_links():
	return {
		'dates': Entry.objects.published().dates('pub_date', 'month'),
	}

@register.filter
def base_site_url(value):                                        
	parsed = urlparse(value)
	return parsed.netloc