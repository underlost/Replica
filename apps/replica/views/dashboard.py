from datetime import datetime, timedelta
from django.template import RequestContext
from django.shortcuts import render_to_response, render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.generic.dates import (ArchiveIndexView, YearArchiveView, MonthArchiveView, DayArchiveView, DateDetailView)
from django.views.generic.list import ListView

from replica.models import Entry, Draft, Topic, Media, EntryType
from replica.forms import EntryModelForm, QuickEntryModelForm, DraftModelForm, TopicModelForm, EntryTypeModelForm, MediaModelForm

def Index(request):
	if request.method == "POST":
		instance = Entry(user=request.user, pub_date=datetime.now)
		f = QuickEntryModelForm(request.POST or None, instance=instance)
		if f.is_valid():
			f.save()
			messages.add_message(
				request, messages.INFO, 'Idea saved.')
			return redirect('Replica:Index')
	else:
		initial = {}
		if "url" in request.GET:
			initial["url"] = request.GET["url"]
		if "title" in request.GET:
			initial["title"] = request.GET["title"].strip()
		if initial:
			f = QuickEntryModelForm(initial=initial)
		else:
			f = QuickEntryModelForm()
	ctx = {'form': f,}
	return render(request, 'replica/dashboard/main.html', ctx)

def EntryNew(request):
	instance = Entry(user=request.user)
	if request.method == "POST":
		f = EntryModelForm(request.POST or None, instance=instance)
		if f.is_valid():
			f.save()
			messages.add_message(
				request, messages.INFO, 'Entry Created.')
			return redirect('Replica:EditEntry', entry_guid=instance.guid)
	else:
		initial = {}
		if "url" in request.GET:
			initial["url"] = request.GET["url"]
		if "title" in request.GET:
			initial["title"] = request.GET["title"].strip()
		if initial:
			f = EntryModelForm(initial=initial, instance=instance)
		else:
			f = EntryModelForm(instance=instance)
	variables = {'form': f, 'adding': True, 'editor': True,}
	return render(request, 'replica/dashboard/editor.html', variables)

def EntryDelete(request, entry_guid):
	entry = get_object_or_404(Entry, guid=entry_guid, user=request.user)
	if request.method == 'POST':
		entry.delete()
		return redirect('Replica:Index')
	return render(request, 'replica/dashboard/delete-confirm.html', {'object': entry, 'content_type': 'Entrty',})

def EntryEdit(request, entry_guid):
	entry = get_object_or_404(Entry, user=request.user, guid=entry_guid)
	f = EntryModelForm(request.POST or None, instance=entry)
	if f.is_valid():
		f.save()
		messages.add_message(
			request, messages.INFO, 'Entry Saved.')
		return redirect('Replica:EditEntry', entry_guid=entry_guid)
	variables = RequestContext(request, {'form': f, 'entry': entry, 'adding': False, 'editor': True,})
	return render_to_response('replica/dashboard/editor.html', variables)

def DraftsForEntry(request, entry_guid):
	entry = get_object_or_404(Entry, guid=entry_guid, user=request.user)
	drafts = Draft.objects.all().filter(entry=entry, user=request.user)
	variables = RequestContext(request, {'entry': entry, 'drafts': drafts,})
	return render_to_response('replica/dashboard/drafts.html', variables)

def DraftView(request, entry_guid, draft_guid):
	entry = get_object_or_404(Entry, guid=entry_guid, user=request.user)
	draft = get_object_or_404(Draft, guid=draft_guid, user=request.user)
	f = DraftModelForm(request.POST or None, instance=draft)
	if f.is_valid():
		f.save()
		messages.add_message(
			request, messages.INFO, 'Draft edited.')
		return redirect('Replica:DraftsForEntry', entry_guid=entry_guid)
	variables = RequestContext(request, {'form': f, 'entry': entry, 'draft': draft,})
	return render_to_response('replica/dashboard/drafts_view.html', variables)

def DraftDelete(request, entry_guid, draft_guid):
	entry = get_object_or_404(Entry, guid=entry_guid, user=request.user)
	draft = get_object_or_404(Draft, guid=draft_guid, entry__guid=entry_guid, user=request.user)
	if request.method == 'POST':
		draft.delete()
		messages.add_message(
			request, messages.INFO, 'Draft deleted.')
		return redirect('Replica:DraftsForEntry', entry_guid=entry_guid)
	return render(request, 'replica/dashboard/delete-confirm.html', {'entry': entry, 'object': draft, 'content_type': 'Draft',})

class ReplicaViewMixin(object):
	date_field = 'pub_date'
	paginate_by = 25
	allow_empty = True
	month_format = "%m"

	def get_queryset(self):
		return Entry.objects.filter(user=self.request.user)

class ReplicaIndexView(ReplicaViewMixin, ArchiveIndexView):
    pass

class ReplicaYearView(ReplicaViewMixin, YearArchiveView):
    pass

class ReplicaMonthView(ReplicaViewMixin, MonthArchiveView):
    pass

class ReplicaDayView(ReplicaViewMixin, DayArchiveView):
    pass

#List of public topics
class TopicsList(ListView):
	paginate_by = 25
	template_name = 'replica/dashboard/topic_list.html'

	def get_queryset(self):
		return Topic.objects.mine(self.request.user).order_by('title')

	def get_context_data(self, **kwargs):
		context = super(TopicsList, self).get_context_data(**kwargs)
		context.update({'pub_date': True, 'heading': 'Topics', 'slug':'topics'})
		return context

#New Topic
def TopicNew(request):
	instance = Topic(user=request.user)
	if request.method == 'POST':
		f = TopicModelForm(request.POST or None, request.FILES, instance=instance)
		if f.is_valid():
			f.save()
			messages.add_message(
				request, messages.INFO, 'New Topic.')
			return redirect('Replica:EditTopic', guid=instance.guid)
	else:
		f = TopicModelForm(instance=instance)
	ctx = {'form': f, 'adding': True}
	return render(request, 'replica/dashboard/edit-topic.html', ctx)

#edit topic
def TopicEdit(request, guid):
	topic = get_object_or_404(Topic, guid=guid, user=request.user)
	if request.method == 'POST':
		f = TopicModelForm(request.POST or None, request.FILES, instance=topic)
		if f.is_valid():
			f.save()
			messages.add_message(
				request, messages.INFO, 'Topic successfully changed.')
			return redirect('Replica:EditTopic', guid=topic.guid)
	else:
		f = TopicModelForm(instance=topic)
	ctx = {'form': f, 'topic': topic, 'adding': False}
	return render(request, 'replica/dashboard/edit-topic.html', ctx)

#Delete Topic
def TopicDelete(request, guid):
	topic = get_object_or_404(Topic, guid=guid, user=request.user)
	if request.method == 'POST':
		topic.delete()
		messages.add_message(request, messages.INFO, 'Topic deleted.')
		return redirect('Replica:Topics')
	return render(request, 'replica/dashboard/delete-confirm.html', {'object': topic, 'content_type': 'Topic',})

#List of my media objects
class MediaList(ListView):
	paginate_by = 25
	template_name = 'replica/dashboard/media_list.html'

	def get_queryset(self):
		if self.request.user.is_staff:
			return Media.objects.all().order_by('title')
		else:
			return Media.objects.filter(user=self.request.user).order_by('title')

	def get_context_data(self, **kwargs):
		context = super(MediaList, self).get_context_data(**kwargs)
		context.update({'media': True,})
		return context

#New Image object
def MediaNew(request):
	instance = Media(user=request.user)
	if request.method == 'POST':
		f = MediaModelForm(request.POST or None, request.FILES, instance=instance)
		if f.is_valid():
			f.save()
			messages.add_message(request, messages.INFO, 'Image Added.')
			return redirect('Replica:EditMedia', guid=instance.guid)
	else:
		f = MediaModelForm(instance=instance)
	ctx = {'form': f, 'adding': True}
	return render(request, 'replica/dashboard/edit-media.html', ctx)

#Edit Image
def MediaEdit(request, guid):
	media = get_object_or_404(Media, guid=guid, user=request.user)
	if request.method == 'POST':
		f = MediaModelForm(request.POST or None, request.FILES, instance=media)
		if f.is_valid():
			f.save()
			messages.add_message(
				request, messages.INFO, 'Media successfully changed.')
			return redirect('Replica:EditMedia', guid=media.guid)
	else:
		f = MediaModelForm(instance=media)
	ctx = {'form': f, 'media': media, 'adding': False}
	return render(request, 'replica/dashboard/edit-media.html', ctx)

#Delete Image
def MediaDelete(request, guid):
	media = get_object_or_404(Media, guid=guid, user=request.user)
	if request.method == 'POST':
		media.delete()
		messages.add_message(request, messages.INFO, 'Image deleted.')
		return redirect('Replica:Media')
	return render(request, 'replica/dashboard/delete-confirm.html', {'object': media, 'content_type': 'Media', })

#List of my EntryType objects
class EntryTypeList(ListView):
	paginate_by = 25
	template_name = 'replica/dashboard/entrytype_list.html'

	def get_queryset(self):
		if self.request.user.is_staff:
			return EntryType.objects.all().order_by('title')
		else:
			return EntryType.objects.filter(user=self.request.user).order_by('title')

	def get_context_data(self, **kwargs):
		context = super(EntryTypeList, self).get_context_data(**kwargs)
		context.update({'media': True,})
		return context

#New EntryType
def EntryTypeNew(request):
	instance = EntryType(user=request.user)
	if request.method == 'POST':
		f = EntryTypeModelForm(request.POST or None, request.FILES, instance=instance)
		if f.is_valid():
			f.save()
			messages.add_message(request, messages.INFO, 'EntryType Added.')
			return redirect('Replica:EditEntryType', guid=instance.guid)
	else:
		f = EntryTypeModelForm(instance=instance)
	ctx = {'form': f, 'adding': True}
	return render(request, 'replica/dashboard/edit-entrytype.html', ctx)

#Edit EntryType
def EntryTypeEdit(request, guid):
	entrytype = get_object_or_404(EntryType, guid=guid, user=request.user)
	if request.method == 'POST':
		f = EntryTypeModelForm(request.POST or None, request.FILES, instance=entrytype)
		if f.is_valid():
			f.save()
			messages.add_message(
				request, messages.INFO, 'Media successfully changed.')
			return redirect('Replica:EditEntryType', guid=instance.guid)
	else:
		f = EntryTypeModelForm(instance=entrytype)
	ctx = {'form': f, 'entrytype': entrytype, 'adding': False}
	return render(request, 'replica/dashboard/edit-entrytype.html', ctx)

#Delete EntryType
def EntryTypeDelete(request, guid):
	entrytype = get_object_or_404(EntryType, guid=guid, user=request.user)
	if request.method == 'POST':
		entrytype.delete()
		messages.add_message(request, messages.INFO, 'Entry Type deleted.')
		return redirect('Replica:EntryTypes')
	return render(request, 'replica/dashboard/delete-confirm.html', {'object': entrytype, 'content_type': 'Entrty Type',})
