from __future__ import absolute_import

from django.conf.urls import *
from . import views
from . import feeds

urlpatterns = patterns('',
	url(r'^$', views.TimelinesListView.as_view(), name = 'Timelines'),
	url(r'^new/$', views.AddTimeline, name = 'NewTimeline'),
	url(r'^(?P<timeline_slug>[-\w]+)/$', views.BlipListView.as_view(), name = "Timeline"),
	url(r'^(?P<timeline_slug>[-\w]+)/edit/$', views.EditTimeline, name = "EditTimeline"),
	url(r'^(?P<timeline_slug>[-\w]+)/post$', views.AddBlip, name = 'Add'),
	url(r'^id/(?P<blip_id>\d+)/edit/$', views.EditBlip, name = 'Edit'),
	url(r'^id/(?P<blip_id>\d+)/delete/$', views.DeleteBlip, name = 'Delete'),
	url(r'^id/(?P<blip_id>\d+)/$', views.SingleBlip, name = 'Blip'),

	url(r'^feeds/public/$', feeds.PublicFeed(), name='Public-RSS'),
	url(r'^feeds/events/$', feeds.TimelinesFeed(), name='Timelines-RSS'),
	url(r'^feeds/(?P<timeline_slug>[-\w]+)/$', feeds.TimelineFeed(), name='Timeline-RSS'),
)
