from __future__ import absolute_import

from django.conf import settings
from django.contrib.syndication.views import Feed
from replica.models import Entry

class KitchenSinkFeed(Feed):
    title = settings.SITE_NAME
    link = settings.SITE_URL
    description = settings.SITE_DESC

    def items(self):
        return Entry.objects.published()[:10]

    def item_pubdate(self, item):
        return item.pub_date

class ArticlesFeed(Feed):
    title = settings.SITE_NAME
    link = settings.SITE_URL
    description = "A Life Well Played | Articles"

    def items(self):
        return Entry.objects.published().filter(post_type='articles')[:10]

    def item_pubdate(self, item):
        return item.pub_date

class LinkedFeed(Feed):
    title = settings.SITE_NAME
    link = settings.SITE_DESC
    description = "A Life Well Played | Linked List"

    def items(self):
        return Entry.objects.published().filter(post_type='linked')[:30]

    def item_pubdate(self, item):
        return item.pub_date
