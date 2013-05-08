import datetime

from django.contrib.sitemaps import Sitemap
from django.contrib.flatpages.models import FlatPage
from .models import Entry, Page
   
class BlogSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return Entry.objects.published()

    def lastmod(self, obj):
        return obj.pub_date


class FlatPageSitemap(Sitemap):

    def changefreq(self, obj):
        return 'weekly'

    def priority(self, obj):
        return 0.5

    def items(self):
        return FlatPage.objects.all()

    def lastmod(self, obj):
        return obj.page.pub_date
