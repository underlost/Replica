from __future__ import absolute_import
from django.conf.urls import *
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page

from . import views as dash_views

urlpatterns = patterns('',

	#Replica Admin
	url(r'^$', login_required(dash_views.Index), name = 'Index'),

	#Entries
	url(r'^posts/(?P<year>\d{4})/(?P<month>\w{1,2})/(?P<day>\w{1,2})/$',
		login_required(dash_views.ReplicaDayView.as_view(template_name='replica/dashboard/post_archive_day.html',)),
		name="PostsDay"),

	url(r'^posts/(?P<year>\d{4})/(?P<month>\w{1,2})/$',
		login_required(dash_views.ReplicaMonthView.as_view(template_name='replica/dashboard/post_archive_month.html',)),
		name="PostsMonth"),

	url(r'^posts/(?P<year>\d{4})/$',
		login_required(dash_views.ReplicaYearView.as_view(template_name='replica/dashboard/post_archive_year.html',)),
		name="PostsYear"),

	url(r'^posts/$',
		login_required(dash_views.ReplicaIndexView.as_view(template_name='replica/dashboard/post_archive.html',)),
		name="Posts"),

	#Topics
	url(r'^topics/$', login_required(dash_views.TopicsList.as_view()), name = "Topics"),
	url(r'^topics/new/$', login_required(dash_views.TopicNew), name = "NewTopic"),
	url(r'^topics/edit/(?P<guid>[\w-]+)/$', login_required(dash_views.TopicEdit), name = "EditTopic"),
	url(r'^topics/delete/(?P<guid>[\w-]+)/$', login_required(dash_views.TopicDelete), name = "DeleteTopic"),
	url(r'^topics/entries/(?P<topic_slug>[\w-]+)/$', login_required(dash_views.EntriesForTopic.as_view()), name = "EntriesByTopic"),

	#Entry Types
	url(r'^entry-types/$', login_required(dash_views.EntryTypeList.as_view()), name = "EntryTypes"),
	url(r'^entry-types/new/$', login_required(dash_views.EntryTypeNew), name = "NewEntryType"),
	url(r'^entry-types/edit/(?P<guid>[\w-]+)/$', login_required(dash_views.EntryTypeEdit), name = "EditEntryType"),
	url(r'^entry-types/delete/(?P<guid>[\w-]+)/$', login_required(dash_views.EntryTypeDelete), name = "DeleteEntryType"),

	#Media
	url(r'^media/$', login_required(dash_views.MediaList.as_view()), name = "Media"),
	url(r'^media/new/$', login_required(dash_views.MediaNew), name = "NewMedia"),
	url(r'^media/edit/(?P<guid>[\w-]+)/$', login_required(dash_views.MediaEdit), name = "EditMedia"),
	url(r'^media/delete/(?P<guid>[\w-]+)/$', login_required(dash_views.MediaDelete), name = "DeleteMedia"),

	#Pages
	url(r'^pages/$', login_required(dash_views.PageList.as_view()), name = "Pages"),

	#Users
	url(r'^users/$', login_required(dash_views.UserList.as_view()), name = 'Users'),

	#Settings

	#Editor
	url(r'^editor/$', login_required(dash_views.EntryNew), name = 'NewEntry'),
	url(r'^editor/(?P<entry_guid>[\w-]+)/$', login_required(dash_views.EntryEdit), name = 'EditEntry'),
	url(r'^editor/(?P<entry_guid>[\w-]+)/delete/$', login_required(dash_views.EntryDelete), name = 'DeleteEntry'),
	url(r'^editor/(?P<entry_guid>[\w-]+)/tree/$', login_required(dash_views.DraftsForEntry), name = 'DraftsForEntry'),
	url(r'^editor/(?P<entry_guid>[\w-]+)/tree/(?P<draft_guid>[\w-]+)/$', login_required(dash_views.DraftView), name = 'Draft'),
	url(r'^editor/(?P<entry_guid>[\w-]+)/tree/(?P<draft_guid>[\w-]+)/delete/$', login_required(dash_views.DraftDelete), name = 'DeleteDraft'),

	#Blips
	url(r'^blips/', include('replica.contrib.blip.dashboard.urls', namespace='Blip')),


)
