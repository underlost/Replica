import logging
import datetime
import markdown
from hashlib import md5
import bleach

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_unicode, smart_str
from django.template.defaultfilters import slugify

from replica.pulse.utils import guid_generator, username_generator

class Post(models.Model):
    guid = models.UUIDField(primary_key=True, max_length=32, default=guid_generator(length=16), editable=False)
    parrent = models.SlugField(max_length=32, blank=True, null=True)
    ip_addr = models.IPAddressField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
    pub_date = models.DateTimeField(verbose_name=_("Post date"), auto_now_add=True)
    is_valid = models.BooleanField(help_text=_("If true, allow followup threads"), default=False)
    is_public = models.BooleanField(help_text=_("If true, list in public index"), default=False)
    body = models.TextField()
    body_html = models.TextField()

    def store(self, request):
        self.ip_addr = request.META['REMOTE_ADDR']
        try:
            self.save()
        except:
            pass

    def save(self, *args, **kwargs):
        self.body_html = bleach.clean(markdown.markdown(smart_unicode(self.body)))
        super(Post, self).save(*args, **kwargs)

class Known_IPs(models.Model):
    post = models.ForeignKey(Post)
    pub_date = models.DateTimeField(auto_now_add=True)
    ip_addr = models.IPAddressField()
    user_agent = models.CharField(max_length=1024, null=True)
    referer = models.CharField(max_length=512, null=True)

    def store(self, request):
        self.user_agent = request.META.get('HTTP_USER_AGENT','')
        self.ip_addr = request.META['REMOTE_ADDR']
        self.referer = request.META.get('HTTP_REFERER','')
        try:
            self.save()
        except:
            pass
