from __future__ import absolute_import
from django.conf.urls import *
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page

from . import views as blip_views

urlpatterns = patterns('',
    url(r'^$', login_required(blip_views.AddBlip), name = 'Index'),
    url(r'^all/$', login_required(blip_views.LatestBlipsListViewMobile.as_view()), name = 'All'),
    url(r'^timelines/$', login_required(blip_views.TimelinesListView.as_view()), name = 'Timelines'),
    url(r'^timelines/new/$', login_required(blip_views.AddTimeline), name = 'NewTimeline'),
    url(r'^timelines/(?P<timeline_slug>[-\w]+)/$', login_required(blip_views.AddBlipToTimeline), name = 'Timeline'),
    url(r'^timelines/(?P<timeline_slug>[-\w]+)/all/$', login_required(blip_views.TimelineBlipListView.as_view()), name = "TimelineAll"),
    url(r'^timelines/(?P<timeline_slug>[-\w]+)/edit/$', login_required(blip_views.EditTimeline), name = 'EditTimeline'),
    url(r'^status/(?P<blip_guid>[-\w]+)/$', login_required(blip_views.SingleBlip), name = 'Blip'),
    url(r'^status/(?P<blip_guid>[-\w]+)/edit/$', login_required(blip_views.EditBlip), name = 'EditBlip'),
    url(r'^status/(?P<blip_guid>[-\w]+)/delete/$', login_required(blip_views.DeleteBlip), name = 'DeleteBlip'),

)
