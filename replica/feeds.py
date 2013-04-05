from __future__ import absolute_import

from django.contrib.syndication.views import Feed
from .models import Entry

class KitchenSinkFeed(Feed):
    title = "underlost, By Tyler Rilling"
    link = "http://underlost.net/"
    description = "Collection of articles and links from around the interwebs."

    def items(self):
        return Entry.objects.published()[:10]

    def item_pubdate(self, item):
        return item.pub_date
        
class ArticlesFeed(Feed):
    title = "underlost, By Tyler Rilling"
    link = "http://underlost.net/"
    description = "Collection of articles from around the interwebs."

    def items(self):
        return Entry.objects.published().filter(post_type='articles')[:10]

    def item_pubdate(self, item):
        return item.pub_date

class LinkedFeed(Feed):
    title = "underlost linked list"
    link = "http://underlost.net/linked/"
    description = "Collection of articles from around the interwebs."

    def items(self):
        return Entry.objects.published().filter(post_type='linked')[:30]

    def item_pubdate(self, item):
        return item.pub_date