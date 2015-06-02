from __future__ import absolute_import

import logging
from django.shortcuts import render_to_response, render, get_object_or_404, redirect
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic.list import ListView

from replica.contrib.blip.models import Timeline, Blip
from replica.contrib.blip.forms import TimelineModelForm, BlipModelForm

class LatestBlipsListViewMobile(ListView):
    paginate_by = 25
    template_name = 'replica/dashboard/blip/blip_list.html'

    def get_queryset(self):
        return Blip.objects.filter(user=self.request.user).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super(LatestBlipsListViewMobile, self).get_context_data(**kwargs)
        context.update({'hide_timeline': True, 'nav_title': 'All Blips',})
        return context

class TimelinesListView(ListView):
    paginate_by = 25
    template_name = 'replica/dashboard/blip/timeline_list.html'

    def get_queryset(self):
        return Timeline.objects.filter(user=self.request.user).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super(TimelinesListView, self).get_context_data(**kwargs)
        context.update({ 'nav_title': 'Timelines',})
        return context

class TimelineBlipListView(ListView):
    paginate_by = 100
    template_name = 'replica/dashboard/blip/blip_list.html'

    def get_queryset(self):
        self.timeline = get_object_or_404(Timeline, slug=self.kwargs.pop('timeline_slug'))
        b = Blip.objects.filter(user=self.request.user).filter(timeline=self.timeline)
        if self.timeline.rev_order == True:
            return b.order_by('-pub_date')
        else:
            return b.order_by('pub_date')

    def get_context_data(self, **kwargs):
        context = super(TimelineBlipListView, self).get_context_data(**kwargs)
        context.update({'timeline': self.timeline, 'nav_title': self.timeline.name,})
        return context

def AddTimeline(request):
    #add a timeline.
    instance = Timeline(user=request.user)
    f = TimelineModelForm(request.POST or None, instance=instance)
    if f.is_valid():
        f.save()
        messages.add_message(
            request, messages.INFO, 'New list created.')
        return redirect('Replica:Blip-Timelines')

    ctx = {'form': f, 'adding': True}
    return render(request, 'replica/dashboard/blip/edit_timeline.html', ctx)

def EditTimeline(request, timeline_slug):
    #Lets a user edit a blip they've previously added.
    timeline = get_object_or_404(Timeline, slug=timeline_slug)
    f = TimelineModelForm(request.POST or None, instance=timeline)
    if f.is_valid():
        f.save()
        return redirect('Replica:Blip-Add-To-Timeline', timeline_slug=timeline_slug)

    ctx = {'form': f, 'timeline': timeline, 'adding': False}
    return render(request, 'replica/dashboard/blip/edit_timeline.html', ctx)

def SingleBlip(request, blip_guid):
	#Shows a single blip.
	blip = get_object_or_404(Blip, guid=blip_guid)
	if blip.timeline:
		recent_blips = Blip.objects.filter(timeline__id=blip.timeline.id, is_private=False)[:5]
		ctx = {'blip': blip, 'recent_blips': recent_blips}
	else:
		ctx = {'blip': blip}
	return render(request, 'replica/dashboard/blip/single_blip.html', ctx)

def AddBlip(request, timeline_slug=None):
    object_list = Blip.objects.filter(user=request.user).order_by('-pub_date')[:10]

    instance = Blip(user=request.user)
    f = BlipModelForm(request.POST or None, instance=instance)
    if f.is_valid():
        f.save()
        messages.add_message(
            request, messages.INFO, 'Blip Added.')
        return redirect('Replica:Blip:Index')

    ctx = {'form': f, 'object_list': object_list, 'adding': True, 'blip_submit': True, 'hide_timeline': True, 'nav_title': 'All Blips', }
    return render(request, 'replica/dashboard/blip/blip_list.html', ctx)

def AddBlipToTimeline(request, timeline_slug):
    ft = get_object_or_404(Timeline, slug=timeline_slug)
    if ft.rev_order == True:
        b = Blip.objects.filter(user=request.user).filter(timeline=ft).order_by('-pub_date')[:10]
    else:
        b = Blip.objects.filter(user=request.user).filter(timeline=ft).order_by('pub_date')[:10]

    instance = Blip(user=request.user, timeline=ft)
    f = BlipModelForm(request.POST or None, instance=instance)
    if f.is_valid():
        f.save()
        messages.add_message(
            request, messages.INFO, 'Blip Added.')
        return redirect('Replica:Blip:Timeline', timeline_slug=timeline_slug)

    ctx = {'form': f, 'timeline': ft, 'adding': True, 'blip_submit': True, 'nav_title': ft.name, 'object_list': b, }
    return render(request, 'replica/dashboard/blip/blip_list.html', ctx)

def EditBlip(request, blip_guid):
    #Lets a user edit a blip they've previously added.
    blip = get_object_or_404(Blip, guid=blip_guid, user=request.user)
    f = BlipModelForm(request.POST or None, instance=blip)
    if f.is_valid():
        f.save()
        return redirect('Replica:Blip:Blip', blip_guid=blip_guid)

    ctx = {'form': f, 'blip': blip, 'adding': False}
    return render(request, 'replica/dashboard/blip/edit_blip.html', ctx)

def DeleteBlip(request, blip_guid):
    blip = get_object_or_404(Blip, guid=blip_guid, user=request.user)
    if request.method == 'POST':
        blip.delete()
        return redirect('Replica:Blip:Index')
    return render(request, 'replica/dashboard/delete-confirm.html', {'object': blip, 'content_type': 'Blip'})
