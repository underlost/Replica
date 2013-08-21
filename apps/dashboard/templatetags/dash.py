from __future__ import absolute_import
import hashlib
from urlparse import urlparse
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.shortcuts import redirect, render, get_object_or_404
from django import template
from wellplayed.apps.replica.models import Entry, Draft, Page

register = template.Library()

@register.inclusion_tag('dashboard/templatetags/render_posts.html')
def render_ideas(num):
	objects = Entry.objects.ideas()[:num]
	return { 'objects': objects, 'color':'orange',}   

@register.inclusion_tag('dashboard/templatetags/render_posts.html')
def render_upcoming(num):
	objects = Entry.objects.upcoming()[:num]
	return { 'objects': objects, 'color':'green',}  

@register.inclusion_tag('dashboard/templatetags/month_links_snippet.html')
def render_dashboard_months():
	dates = Entry.objects.all().dates('pub_date', 'month')
	return { 'dates': dates, }