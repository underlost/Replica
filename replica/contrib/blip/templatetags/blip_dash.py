from __future__ import absolute_import
from urlparse import urlparse
import hashlib

from django import template
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from django.template import RequestContext

from ..models import Timeline, Blip

register = template.Library()

@register.inclusion_tag('replica/dashboard/blip/templatetags/latest_timelines.html')
def render_timelines(user, num):
	objects = Timeline.objects.filter(user__username=user)[:num]
	return {'objects': objects,}


@register.inclusion_tag('replica/dashboard/blip/templatetags/latest_blips.html')
def render_latest_blips(username, timelineID=None, num=500):
	if timelineID:
		objects = Blip.objects.filter(user=username).filter(timeline__id=timelineID)[:num]
	else:
		objects = Blip.objects.filter(user=username)[:num]
	return { 'objects': objects, }

@register.simple_tag
def render_blip_counts(username):
	obj_count = Blip.objects.filter(user=username).count()
	return obj_count

@register.simple_tag
def render_timeline_counts(username):
	obj_count = Timeline.objects.filter(user=username).count()
	return obj_count

@register.inclusion_tag('replica/dashboard/blip/templatetags/latest_blip_time.html')
def render_latest_timestamp(username, timelineID=None):
	if timelineID:
		latest_obj = Blip.objects.filter(user=username).filter(timeline__id=timelineID)[:1]
	else:
		latest_obj = Blip.objects.filter(user=username)[:1]
	return { 'latest_obj': latest_obj, }
