import logging
import datetime
import markdown
from hashlib import md5

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_unicode, smart_str
from django.template.defaultfilters import slugify

class BlipManager(models.Manager):

	def published(self):
		return self.public().filter(pub_date__lte=datetime.datetime.now())

	def public(self):
		return super(BlipManager, self).get_query_set().filter(is_private=False)


class Timeline(models.Model):
	name = models.CharField(max_length=250)
	slug = models.SlugField(max_length=250, unique=True)
	is_public = models.BooleanField(help_text=_("Should be checked you want anyone to see"), default=True)
	rev_order = models.BooleanField(help_text=_("Reverse order of list displayed? (Newest on top)"), default=False)
	pub_date = models.DateTimeField(verbose_name=_("Creation date"), auto_now_add=True)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='timelines')
	guid = models.CharField(max_length=32, unique=True)

	def __unicode__(self):
		return "%s" % (self.name)

	class Meta:
		db_table = 'blip_timelines'
		verbose_name_plural = 'timelines'
		ordering = ('-pub_date',)
		get_latest_by = 'pub_date'
		unique_together = (('slug','user'),)

	def items(self):
		return Blip.objects.filter(timeline=self)

	def item_count(self):
		item_counts = Blip.objects.filter(timeline=self).count()
		return item_counts

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.name)
		if not self.guid:
			#GUID Generation
			guid_base = "%s-%s" % (self.name, datetime.datetime.now())
			guid_encoded = guid_base.encode('ascii', 'ignore')
			guid = md5(guid_encoded).hexdigest()[:16]
			self.guid = guid
		super(Timeline, self).save(*args, **kwargs)

class Blip(models.Model):
	body = models.TextField()
	body_html = models.TextField()
	pub_date = models.DateTimeField(verbose_name=_("Date posted"), auto_now_add=True)
	is_private = models.BooleanField(help_text=_("Should be checked if no one else should see this."), default=False)
	timeline = models.ForeignKey(Timeline, blank=True, null=True)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='blips')
	guid = models.CharField(max_length=32, unique=True)
	objects = BlipManager()

	def __unicode__(self):
		return self.body_html

	class Meta:
		db_table = 'blip_blips'
		verbose_name_plural = 'blips'
		ordering = ('-pub_date',)
		get_latest_by = 'pub_date'

	def save(self, *args, **kwargs):
		self.body_html = markdown.markdown(smart_unicode(self.body))
		if not self.guid:
			#GUID Generation
			guid_base = "%s-%s" % (self.body[:96], datetime.datetime.now())
			guid_encoded = guid_base.encode('ascii', 'ignore')
			guid = md5(guid_encoded).hexdigest()[:16]
			self.guid = guid
		super(Blip, self).save(*args, **kwargs)
