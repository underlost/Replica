from __future__ import absolute_import
from django.shortcuts import render_to_response, render, get_object_or_404, redirect
from django import template

from core.models import Account
from replica.models import Topic, Entry

register = template.Library()

@register.inclusion_tag('replica/pulse/templatetags/render_latest_entries.html')
def render_latest_entries(num):
	objects = Entry.objects.all()[:num]
	return { 'objects': objects, }   

@register.inclusion_tag('replica/pulse/templatetags/render_articles.html')
def render_latest_articles():
	objects = Entry.objects.published().exclude(post_type__slug='linked')
	return { 'objects': objects, }   

@register.inclusion_tag('replica/pulse/templatetags/month_links_snippet.html')
def render_month_links():
	dates = Entry.objects.published().dates('pub_date', 'month')
	return { 'dates': dates, }