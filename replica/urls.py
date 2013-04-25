from __future__ import absolute_import
from django.conf.urls.defaults import *
from django.views.generic import TemplateView
from . import views
from . import feeds

urlpatterns = patterns('',

	#Replica Admin
	url(r'^dashboard/$', views.ReplicaAdmin, name = 'replica-admin'),
	url(r'^dashboard/create/$', views.ReplicaCreate, name = 'replica-add'),
	url(r'^dashboard/nano/$', views.Replica_Nano, name = 'replica-nano'),
	url(r'^dashboard/edit/(?P<entry_id>\d+)/$', views.ReplicaEdit, name = 'replica-edit'),
	url(r'^dashboard/delete/(?P<entry_id>\d+)/$', views.ReplicaDelete, name = 'replica-delete'),
	url(r'^dashboard/drafts/(?P<entry_id>\d+)/$', views.ReplicaDrafts, name = 'replica-drafts'),
	url(r'^dashboard/drafts/(?P<entry_id>\d+)/(?P<draft_id>\d+)/$', views.ReplicaDraftsView, name = 'replica-draft-view'),
	url(r'^dashboard/drafts/delete/(?P<draft_id>\d+)/$', views.ReplicaDraftDelete, name = 'replica-draft-delete'),
	url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'replica/admin/login.html'}),
	
	#Articles
	url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[\w-]+)/$', views.ReplicaEntryDetail, name="entry_detail"),
	url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$', views.ReplicaDayArchiveView.as_view(), name="entry_day"),
	url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/$', views.ReplicaMonthArchiveView.as_view(), name="entry_month"),
	url(r'^(?P<year>\d{4})/$', views.ReplicaYearArchiveView.as_view(), name="entry_year"),
	url(r'^?$', views.ReplicaArchiveIndexView.as_view(), name="news_index"),
	 
	#RSS Feeds
	url(r'^feed/$', feeds.KitchenSinkFeed(), name='Kitchensink-rss'),
	   
	#Pages
	#(r'^(?P<slug>[\w-]+)/$', views.ReplicaPage),
)