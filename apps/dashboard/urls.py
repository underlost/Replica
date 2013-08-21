from __future__ import absolute_import
from django.conf.urls.defaults import *
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page

from . import views

urlpatterns = patterns('',

	#Replica Admin
	url(r'^$', login_required(views.ReplicaAdmin), name = 'replica-admin'),

	#entries
	url(r'^entries/(?P<year>\d{4})/(?P<month>\w{1,2})/(?P<day>\w{1,2})/$', login_required(views.ReplicaAdminDayArchiveView.as_view(template_name='dashboard/entry_archive_day.html',)), name="replica-entries-day"),
	url(r'^entries/(?P<year>\d{4})/(?P<month>\w{1,2})/$', login_required(views.ReplicaAdminMonthArchiveView.as_view(template_name='dashboard/entry_archive_month.html',)), name="replica-entries-month"),
	url(r'^entries/(?P<year>\d{4})/$', login_required(views.ReplicaAdminYearArchiveView.as_view(template_name='dashboard/entry_archive_year.html',)), name="replica-entries-year"),
	url(r'^entries/$', login_required(views.ReplicaAdminArchiveIndexView.as_view(template_name='dashboard/entry_archive.html',)), name="replica-entries"),
	
	#drafts
	url(r'^drafts/(?P<entry_id>\d+)/$', login_required(views.ReplicaDrafts), name = 'replica-drafts'),
	url(r'^drafts/(?P<entry_id>\d+)/(?P<draft_id>\d+)/$', login_required(views.ReplicaDraftsView), name = 'replica-draft-view'),
	
	url(r'^nano/$', login_required(views.Replica_Nano), name = 'replica-nano'),
	url(r'^pages/$', login_required(views.ReplicaPageListView.as_view()), name = 'replica-pages'),
	
	#create
	url(r'^create/entry$', login_required(views.ReplicaCreate), name = 'replica-add'),
	url(r'^create/page/$', login_required(views.ReplicaPage), name = 'replica-add-page'),
	
	#edit
	url(r'^edit/entry/(?P<entry_id>\d+)/$', login_required(views.ReplicaEdit), name = 'replica-edit'),
	url(r'^edit/page/(?P<page_id>\d+)/$', login_required(views.ReplicaPageEdit), name = 'replica-page-edit'),
	
	#delete
	url(r'^delete/entry/(?P<entry_id>\d+)/$', login_required(views.ReplicaDelete), name = 'replica-delete'),
	url(r'^delete/draft/(?P<draft_id>\d+)/$', login_required(views.ReplicaDraftDelete), name = 'replica-draft-delete'),
)