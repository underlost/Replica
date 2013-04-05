from __future__ import absolute_import
from django.conf.urls.defaults import *
from django.views.generic import TemplateView
from . import views
from . import feeds

urlpatterns = patterns('',

	#Replica Admin
	url(r'^replicate/$', views.ReplicaAdmin, name = 'replica-admin'),
	url(r'^replicate/create/$', views.ReplicaCreate, name = 'replica-add'),
	url(r'^replicate/edit/(?P<entry_id>\d+)/$', views.ReplicaEdit, name = 'replica-edit'),
	url(r'^replicate/delete/(?P<entry_id>\d+)/$', views.ReplicaDelete, name = 'replica-delete'),
	(r'^r19/$', 'django.contrib.auth.views.login', {'template_name': 'replica/admin/login.html'}),
	
	#Articles
	url(r'^blog/(?P<slug>[\w-]+)/$', views.entry_detail, name="entry_detail"),
	url(r'^blog/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$', views.ReplicaDayArchiveView.as_view(), name="blog_day"),
	url(r'^blog/(?P<year>\d{4})/(?P<month>[a-z]{3})/$', views.ReplicaMonthArchiveView.as_view(), name="blog_month"),
	url(r'^blog/(?P<year>\d{4})/$', views.ReplicaYearArchiveView.as_view(), name="blog_year"),
	url(r'^blog/?$', views.ReplicaArchiveIndexView.as_view(), name="blog-index"),
	 
	#RSS Feeds
	url(r'^feed/$', feeds.KitchenSinkFeed(), name='Kitchensink-rss'),
   
	#Homepage
	url(r'^$', views.Index, name="Index"),
	   
	#Pages
	#(r'^(?P<slug>[\w-]+)/$', views.page),
)