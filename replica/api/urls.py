from __future__ import absolute_import

from django.conf.urls import *
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from coreExtend import api as core_api
from replica.pulse import  api as pulse_api
from replica.contrib.blip import api as blip_api

class SimpleStaticView(TemplateView):
    def get_template_names(self):
        return "replica/api/%s.html" % (self.kwargs.get('template_name'))

    def get(self, request, *args, **kwargs):
        return super(SimpleStaticView, self).get(request, *args, **kwargs)

blip_urls = patterns('',
    url(r'^timelines/(?P<slug>[0-9a-zA-Z_-]+)$', blip_api.TimelineDetail.as_view(), name='timeline-detail'),
    url(r'^timelines/(?P<slug>[0-9a-zA-Z_-]+)/list$', blip_api.TimelineBlipList.as_view(), name='timeline-blip-list'),
    url(r'^timelines$', blip_api.TimelineList.as_view(), name='timeline-list'),
    url(r'^new/blip$', blip_api.BlipCreate.as_view(), name='blip-new'),
    url(r'^new/timeline$', blip_api.TimelineCreate.as_view(), name='timeline-new'),
    url(r'^status/(?P<guid>[0-9a-zA-Z_-]+)$', blip_api.BlipDetail.as_view(), name='blip-detail'),
    url(r'^all$', blip_api.BlipList.as_view(), name='blip-list'),
)

urlpatterns = patterns('',
    # Pulse
    url(r'^topics$', pulse_api.TopicList.as_view(), name='topic-list'),
    url(r'^topics/(?P<slug>[0-9a-zA-Z_-]+)$', pulse_api.TopicDetail.as_view(), name='topic-detail'),
    url(r'^topics/(?P<slug>[0-9a-zA-Z_-]+)/entries$', pulse_api.TopicEntryList.as_view(), name='topic-entries-list'),
    url(r'^entrytypes$', pulse_api.EntryTypeList.as_view(), name='entrytype-list'),
    url(r'^entrytypes/(?P<slug>[0-9a-zA-Z_-]+)$', pulse_api.EntryTypeDetail.as_view(), name='entrytype-detail'),
    url(r'^entrytypes/(?P<slug>[0-9a-zA-Z_-]+)/entries$', pulse_api.EntryTypeEntryList.as_view(), name='entrytype-entries-list'),
    url(r'^entries$', pulse_api.EntryList.as_view(), name='entry-list'),
    url(r'^entries/drafts$', pulse_api.EntryDraftList.as_view(), name='entry-drafts-list'),
    url(r'^entries/upcoming$', pulse_api.EntryUpcomingList.as_view(), name='entry-upcoming-list'),
    url(r'^entry/(?P<guid>[0-9a-zA-Z_-]+)$', pulse_api.EntryDetail.as_view(), name='entry-detail'),
    url(r'^pages$', pulse_api.PageList.as_view(), name='page-list'),
    url(r'^page/(?P<guid>[0-9a-zA-Z_-]+)$', pulse_api.PageDetail.as_view(), name='page-detail'),

    # contrib.blip
    url(r'^blip/', include(blip_urls)),
    url(r'^users/(?P<username>[0-9a-zA-Z_-]+)/timelines$', blip_api.UserTimelineList.as_view(), name='user-timeline-list'),
    url(r'^users/(?P<username>[0-9a-zA-Z_-]+)/blip$', blip_api.UserBlipList.as_view(), name='user-blip-list'),

    # Users
    url(r'^users/(?P<username>[0-9a-zA-Z_-]+)$', core_api.UserDetail.as_view(), name='user-detail'),
    url(r'^users$', core_api.UserList.as_view(), name='user-list'),
    url(r'^current$', core_api.CurrentUser.as_view(), name='user-current'),

    #Static
    #url(r'^(?P<template_name>\w+)$', login_required(SimpleStaticView.as_view()), name='api'),
    url(r'^$', TemplateView.as_view(template_name="replica/api/index.html"), name='API-Index'),
)
