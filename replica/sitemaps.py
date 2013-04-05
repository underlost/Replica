import datetime

from django.contrib.sitemaps import Sitemap
from django.contrib.flatpages.models import FlatPage
from .models import Entry, Page

class DirectToTemplateSitemap(Sitemap):
  changefreq = "daily"

  def __init__(self, patterns):
    self.patterns = patterns

  def items(self):
    return [p for p in self.patterns if p.callback 
               and p.callback.__module__ == 'django.views.generic.simple'
               and p.callback.func_name == 'direct_to_template']

  def changefreq(self, obj):
    return 'daily'

  def lastmod(self, obj):
    return datetime.datetime.now()

  def location(self, obj):
    url = obj.regex.pattern.replace('^', '/').replace('$','')
    return url
    
class BlogSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return Entry.objects.published()

    def lastmod(self, obj):
        return obj.pub_date


class FlatPageSitemap(Sitemap):

    def changefreq(self, obj):
        if obj.url.startswith('/replicate/'):
            return 'never' # Old documentation never changes.
        else:
            return 'weekly'

    def priority(self, obj):
        if obj.url.startswith('/replicate/'):
            return 0.1 # Old documentation gets a low priority.
        else:
            return 0.5

    def items(self):
        return FlatPage.objects.all()

    def lastmod(self, obj):
        return obj.page.pub_date
