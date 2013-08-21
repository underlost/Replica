from __future__ import absolute_import
from django.conf.urls.defaults import *
from django.views.generic import TemplateView
from django.views.decorators.cache import cache_page

from . import views
from . import feeds

urlpatterns = patterns('',	
	
	#Articles
	url(r'^featured/(?P<slug>[\w-]+)/$', views.ReplicaEntryFeatured, name="entry_featured"),
	url(r'^(?P<year>\d{4})/(?P<month>\w{1,2})/(?P<day>\w{1,2})/(?P<slug>[\w-]+)/$', cache_page(900)(views.ReplicaDateDetailView.as_view()), name="entry_detail"),
	url(r'^(?P<year>\d{4})/(?P<month>\w{1,2})/(?P<day>\w{1,2})/$', cache_page(900)(views.ReplicaDayArchiveView.as_view()), name="entry_day"),
	url(r'^(?P<year>\d{4})/(?P<month>\w{1,2})/$', cache_page(900)(views.ReplicaMonthArchiveView.as_view()), name="entry_month"),
	url(r'^(?P<year>\d{4})/$', cache_page(900)(views.ReplicaYearArchiveView.as_view()), name="entry_year"),
	url(r'^$', views.ReplicaArchiveIndexView.as_view(), name="entry_index"),
	
	#Static
	url(r'^archive/$', TemplateView.as_view(template_name="replica/archive.html")),
	 
	#RSS Feeds
	url(r'^feed/$', feeds.KitchenSinkFeed(), name='Kitchensink-rss'),
)