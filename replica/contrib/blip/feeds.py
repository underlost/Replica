from __future__ import absolute_import

from django.core import urlresolvers
from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404
from django.conf import settings
from .models import Timeline, Blip

class PublicFeed(Feed):
    title = 'Blips'
    link = '/feeds/public/'
    description = 'All public updates.'

    def items(self):
        return Blip.objects.published()[:10]

    def item_pubdate(self, item):
        return item.pub_date

class TimelinesFeed(Feed):
    title = settings.SITE_NAME
    link = '/feeds/timelines/'
    description = "Timelines"

    def items(self):
        return Timeline.objects.published()[:10]

    def item_pubdate(self, item):
        return item.pub_date

class TimelineFeed(Feed):

    def title(self, obj):
        self.timeline = get_object_or_404(Timeline, slug=self.kwargs.pop('timeline_slug'))
        return 'Updates for %s' % (self.timeline.name)

    def link(self, obj):
        self.timeline = get_object_or_404(Timeline, slug=self.kwargs.pop('timeline_slug'))
        return '/feeds/%s/' % (self.timeline.slug)

    def description(self, obj):
        self.timeline = get_object_or_404(Timeline, slug=self.kwargs.pop('timeline_slug'))
        return 'Blips for %s' % (self.timeline.name)

    def items(self):
        self.timeline = get_object_or_404(Timeline, slug=self.kwargs.pop('timeline_slug'))
        b = Blip.objects.filter(timeline=self.timeline, is_private=False)
        if self.timeline.rev_order == True:
            return b.order_by('-pub_date')[:30]
        else:
            return b.order_by('pub_date')[:30]

    def item_pubdate(self, item):
        return item.pub_date
