from __future__ import absolute_import
from django.conf.urls import *
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page

from replica.views import dashboard as views

urlpatterns = patterns('',

	#Replica Admin
	url(r'^$', login_required(views.Index), name = 'Index'),

	#Entries
	url(r'^entries/(?P<year>\d{4})/(?P<month>\w{1,2})/(?P<day>\w{1,2})/$', login_required(views.ReplicaDayView.as_view(template_name='replica/dashboard/entry_archive_day.html',)), name="EntriesDay"),
	url(r'^entries/(?P<year>\d{4})/(?P<month>\w{1,2})/$', login_required(views.ReplicaMonthView.as_view(template_name='replica/dashboard/entry_archive_month.html',)), name="EntriesMonth"),
	url(r'^entries/(?P<year>\d{4})/$', login_required(views.ReplicaYearView.as_view(template_name='replica/dashboard/entry_archive_year.html',)), name="EntriesYear"),
	url(r'^entries/$', login_required(views.ReplicaIndexView.as_view(template_name='replica/dashboard/entry_archive.html',)), name="Entries"),

	#Topics
	url(r'^topics/$', login_required(views.TopicsList.as_view()), name = "Topics"),
	url(r'^topics/new/$', login_required(views.TopicNew), name = "NewTopic"),
	url(r'^topics/edit/(?P<guid>[\w-]+)/$', login_required(views.TopicEdit), name = "EditTopic"),
	url(r'^topics/delete/(?P<guid>[\w-]+)/$', login_required(views.TopicDelete), name = "DeleteTopic"),

	#Entry Types
	url(r'^entry-types/$', login_required(views.EntryTypeList.as_view()), name = "EntryTypes"),
	url(r'^entry-types/new/$', login_required(views.EntryTypeNew), name = "NewEntryType"),
	url(r'^entry-types/edit/(?P<guid>[\w-]+)/$', login_required(views.EntryTypeEdit), name = "EditEntryType"),
	url(r'^entry-types/delete/(?P<guid>[\w-]+)/$', login_required(views.EntryTypeDelete), name = "DeleteEntryType"),

	#Media
	url(r'^media/$', login_required(views.MediaList.as_view()), name = "Media"),
	url(r'^media/new/$', login_required(views.MediaNew), name = "NewMedia"),
	url(r'^media/edit/(?P<guid>[\w-]+)/$', login_required(views.MediaEdit), name = "EditMedia"),
	url(r'^media/delete/(?P<guid>[\w-]+)/$', login_required(views.MediaDelete), name = "DeleteMedia"),

	#Editor
	url(r'^editor/$', login_required(views.EntryNew), name = 'NewEntry'),
	url(r'^editor/(?P<entry_guid>[\w-]+)/$', login_required(views.EntryEdit), name = 'EditEntry'),
	url(r'^editor/(?P<entry_guid>[\w-]+)/delete/$', login_required(views.EntryDelete), name = 'DeleteEntry'),
	url(r'^editor/(?P<entry_guid>[\w-]+)/tree/$', login_required(views.DraftsForEntry), name = 'DraftsForEntry'),
	url(r'^editor/(?P<entry_guid>[\w-]+)/tree/(?P<draft_guid>[\w-]+)/$', login_required(views.DraftView), name = 'Draft'),
	url(r'^editor/(?P<entry_guid>[\w-]+)/tree/(?P<draft_guid>[\w-]+)/delete/$', login_required(views.DraftDelete), name = 'DeleteDraft'),

)
