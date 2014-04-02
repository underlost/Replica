from django.template import RequestContext
from django.shortcuts import render_to_response, render, get_object_or_404
from django.views.decorators.cache import cache_page
from django.views.generic.list import ListView
from django.views.generic.dates import (ArchiveIndexView, YearArchiveView, MonthArchiveView, DayArchiveView, DateDetailView)
from django.http import HttpResponseRedirect, HttpResponse

from core.models import Account
from replica.models import Topic, Entry

class PulseViewMixin(object):

	date_field = 'pub_date'
	paginate_by = 25
	month_format = "%m"

	def get_allow_future(self):
		return self.request.user.is_staff

	def get_queryset(self):
		if self.request.user.is_staff:
			return Entry.objects.all()
		else:
			return Entry.objects.published()

class ArchiveIndexView(PulseViewMixin, ArchiveIndexView):
    pass

class YearArchiveView(PulseViewMixin, YearArchiveView):
    pass

class MonthArchiveView(PulseViewMixin, MonthArchiveView):
    pass

class DayArchiveView(PulseViewMixin, DayArchiveView):
    pass

def EntryDetail(request, year, month, slug):
	entry = get_object_or_404(Entry, pub_date__year=year, pub_date__month=month, slug=slug,)
	if request.user.is_staff or entry.is_published:
		template = ['replica/pulse/entries/%s.html' % entry.slug, 'replica/pulse/entry_detail.html']
	else:
		template = ['replica/error.html', '404.html',]
	variables = RequestContext(request, {'object': entry, 'detailed': True,})
	return render_to_response(template, variables)

#Entries for topic
class EntriesForTopic(ListView):
	paginate_by = 20
	template_name = 'replica/pulse/topic_entry_list.html'

	def get_queryset(self):
		self.topic = get_object_or_404(Topic, slug=self.kwargs.pop('topic_slug'))
		return Entry.objects.published().filter(topic=self.topic).order_by('-pub_date')

	def get_context_data(self, **kwargs):
		context = super(EntriesForTopic, self).get_context_data(**kwargs)
		context.update({'topic' : self.topic, 'is_topic': True,})
		return context

#List of public topics
class TopicsList(ListView):
	paginate_by = 25
	template_name = 'replica/pulse/topic_list.html'

	def get_queryset(self):
		return Topic.objects.public().order_by('title')

	def get_context_data(self, **kwargs):
		context = super(TopicsList, self).get_context_data(**kwargs)
		context.update({'topic': False, 'display_new_post': True,})
		return context

#Topic entry redirect
def TopicEntry(request, topic_slug, guid):
	entry = get_object_or_404(Entry, topic__slug=topic_slug, guid=guid,)
	return HttpResponseRedirect(entry.get_absolute_url())
