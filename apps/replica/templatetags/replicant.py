from __future__ import absolute_import
import hashlib
from urlparse import urlparse
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.shortcuts import redirect, render, get_object_or_404
from django import template
from ..models import Entry, Draft, Page

register = template.Library()

@register.inclusion_tag('replica/templatetags/render_latest_entries.html')
def render_latest_entries(num):
	objects = Entry.objects.all()[:num]
	return { 'objects': objects, }   

@register.inclusion_tag('replica/templatetags/render_articles.html')
def render_latest_articles():
	objects = Entry.objects.published().filter(post_type='article')
	return { 'objects': objects, }   

@register.inclusion_tag('replica/templatetags/month_links_snippet.html')
def render_month_links():
	dates = Entry.objects.published().dates('pub_date', 'month')
	return { 'dates': dates, }

@register.filter
def base_site_url(value):                                        
	parsed = urlparse(value)
	return parsed.netloc
	
@register.filter
def email_hash(value):
	u = get_object_or_404(User, username=value)
	a = hashlib.md5(u.email).hexdigest()                                       
	return a