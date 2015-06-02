from __future__ import absolute_import
from urlparse import urlparse
import hashlib

from django import template
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from django.template import RequestContext

from ..models import Timeline, Blip

register = template.Library()

@register.inclusion_tag('blip/templatetags/lists.html')
def render_lists(user, num):
	objects = Timeline.objects.filter(user__username=user)[:num]
	return {'objects': objects,}


@register.inclusion_tag('blip/templatetags/render_blips.html')
def render_latest_blips(num):
	objects = Blip.objects.filter(timeline=num)
	return { 'objects': objects, }

@register.inclusion_tag('blip/templatetags/render_blips_mobile.html')
def render_latest_blips_mobile(user, num):
	objects = Blip.objects.filter(timeline=num).filter(user__username=user)
	return { 'objects': objects, }
