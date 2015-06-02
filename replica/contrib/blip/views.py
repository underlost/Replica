from __future__ import absolute_import

import logging
from django.shortcuts import render_to_response, render, get_object_or_404, redirect
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic.list import ListView

from .models import Timeline, Blip
from .forms import TimelineModelForm, BlipModelForm

class TimelinesListView(ListView):
	paginate_by = 25
	template_name = 'replica/contrib/blip/timeline_list.html'

	def get_queryset(self):
		return Timeline.objects.order_by('-pub_date')

	def get_context_data(self, **kwargs):
		context = super(TimelinesListView, self).get_context_data(**kwargs)
		context.update({})
		return context

class BlipListView(ListView):
	paginate_by = 100
	template_name = 'replica/contrib/blip/blip_list.html'

	def get_queryset(self):
		self.timeline = get_object_or_404(Timeline, slug=self.kwargs.pop('timeline_slug'))
		if self.request.user.is_staff:
			b = Blip.objects.filter(timeline=self.timeline)
		else:
			b = Blip.objects.filter(timeline=self.timeline, is_private=False)
		if self.timeline.rev_order == True:
			return b.order_by('-pub_date')
		else:
			return b.order_by('pub_date')

	def get_context_data(self, **kwargs):
		context = super(BlipListView, self).get_context_data(**kwargs)
		context.update({'timeline': self.timeline,})
		return context

class LatestBlipListView(ListView):
	paginate_by = 100
	template_name = 'replica/contrib/blip/blip_list.html'

	def get_queryset(self):
		if self.request.user.is_staff:
			return Blip.objects.order_by('pub_date')
		else:
			return Blip.objects.order_by('pub_date').filter(is_private=False)

	def get_context_data(self, **kwargs):
		context = super(LatestBlipListView, self).get_context_data(**kwargs)
		return context

def SingleBlip(request, blip_id):
	#Shows a single blip.
	blip = get_object_or_404(Blip, pk=blip_id)
	ctx = {'blip': blip}
	return render(request, 'replica/contrib/blip/blip.html', ctx)


@login_required
def AddBlip(request, timeline_slug):
	#Lets user add new enties to a list.
	ft = get_object_or_404(Timeline, slug=timeline_slug)
	instance = Blip(user=request.user, timeline=ft)
	f = BlipModelForm(request.POST or None, instance=instance)
	if f.is_valid():
		f.save()
		messages.add_message(
			request, messages.INFO, 'Blip Added.')
		return redirect('Blips:Add', timeline_slug=timeline_slug)

	ctx = {'form': f, 'timeline': ft, 'adding': True}
	return render(request, 'replica/contrib/blip/edit-blip.html', ctx)

@login_required
def AddTimeline(request):
	#add a timeline.
	instance = Timeline(user=request.user)
	f = TimelineModelForm(request.POST or None, instance=instance)
	if f.is_valid():
		f.save()
		messages.add_message(
			request, messages.INFO, 'New list created.')
		return redirect('Blips:Timelines')

	ctx = {'form': f, 'adding': True}
	return render(request, 'replica/contrib/blip/edit-timeline.html', ctx)

@login_required
def EditTimeline(request, timeline_slug):
	#Lets a user edit a blip they've previously added.
	timeline = get_object_or_404(Timeline, slug=timeline_slug)
	f = TimelineModelForm(request.POST or None, instance=timeline)
	if f.is_valid():
		f.save()
		return redirect('Blips:Timeline', timeline_slug=timeline_slug)
	ctx = {'form': f, 'timeline': timeline, 'adding': False}
	return render(request, 'replica/contrib/blip/edit-timeline.html', ctx)

@login_required
def EditBlip(request, blip_id):
	#Lets a user edit a blip they've previously added.
	blip = get_object_or_404(Blip, pk=blip_id, user=request.user)
	f = BlipModelForm(request.POST or None, instance=blip)
	if f.is_valid():
		f.save()
		return redirect('Blips:Timeline', timeline_slug=timeline_slug)

	ctx = {'form': f, 'blip': blip, 'adding': False}
	return render(request, 'replica/contrib/blip/edit-blip.html', ctx)

@login_required
def DeleteBlip(request, blip_id):
	#Lets a user delete an blip they've previously added.
	#Only entries the user "owns" can be deleted.
	blip = get_object_or_404(Blip, pk=blip_id, user=request.user)
	if request.method == 'POST':
		blip.delete()
		return redirect('Blips:Timelines')
	return render(request, 'replica/contrib/blip/delete-confirm.html', {'blip': blip})
