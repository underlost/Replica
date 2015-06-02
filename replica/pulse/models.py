import os
import urllib2
from urlparse import urlparse
from cStringIO import StringIO
from PIL import Image
import markdown
import datetime
from time import strftime
from hashlib import md5
import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from django.utils.encoding import smart_unicode, smart_str
from django.conf import settings

from django.core.urlresolvers import get_script_prefix
from django.utils.encoding import iri_to_uri

from .managers import TopicManager, EntryManager
from .utils import create_thumbnail, guid_generator

CONTENT_FORMAT_CHOICES = ((u'markdown', u'Markdown'), (u'html', u'Raw HTML'),)
IS_ACTIVE_CHOICES = ((True, 'Published'), (False, 'Draft'))
CAN_SUBMIT_CHOICES = ((True, 'Everyone'), (False, 'Only users I allow.'))
IS_PUBLIC_CHOICES = ((True, 'Everyone'), (False, 'No one'))

def upload_topic(instance, filename):
	user_guid = guid_generator(instance.user.id)
	return 'user_uploads/%s/topics/%s' % (user_guid, filename)

def upload_topic_thumb(instance, filename):
	user_guid = guid_generator(instance.user.id)
	return 'user_uploads/%s/topics/thumbnails/%s' % (user_guid, filename)

def media_original(instance, filename):
	user_guid = guid_generator(instance.user.id)
	return 'user_uploads/%s/media/%s' % (user_guid, filename)

def media_thumb(instance, filename):
	user_guid = guid_generator(instance.user.id)
	return 'user_uploads/%s/media/thumbnails/%s' % (user_guid, filename)

class Topic(models.Model):
	title = models.CharField(max_length=255)
	slug = models.SlugField(max_length=255, unique=True)
	description = models.TextField(max_length=1020)
	pub_date = models.DateTimeField(auto_now_add=True)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='owner')
	members = models.ManyToManyField(settings.AUTH_USER_MODEL, db_table='r_Topic_Members', blank=True, related_name='topics', related_query_name='topic')
	is_public = models.BooleanField(help_text=_("Can everyone see this Topic?"), choices=IS_PUBLIC_CHOICES, default=True)
	image = models.ImageField(upload_to=upload_topic, blank=True)
	thumbnail = models.ImageField(upload_to=upload_topic_thumb, blank=True)
	guid = models.CharField(max_length=32, unique=True)

	objects = TopicManager()

	class Meta:
		db_table = 'r_Topic'
		verbose_name_plural = 'topics'
		ordering = ['-title']
		get_latest_by = 'pub_date'

	def __unicode__(self):
		return "%s" % (self.title,)

	def entry_count(self):
		entry_total = Entry.objects.filter(topic=self).count()
		return entry_total

	def save(self, *args, **kwargs):
		if self.image and not self.thumbnail:
			create_thumbnail(self.image)
		if not self.id:
			self.slug = slugify(self.title)
			#GUID Generation
			guid_base = str(uuid.uuid4())
			guid_encoded = guid_base.encode('ascii', 'ignore')
			guid = md5(guid_encoded).hexdigest()[:16]
			self.guid = guid
		super(Topic, self).save(*args, **kwargs)

class Media(models.Model):
	title = models.CharField(max_length=510)
	pub_date = models.DateTimeField(auto_now_add=True)
	description = models.CharField(max_length=510, blank=True)
	url = models.URLField(blank=True)
	image = models.ImageField(upload_to=media_original, blank=True, null=True)
	thumbnail = models.ImageField(upload_to=media_thumb, blank=True, null=True)
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	guid = models.CharField(max_length=32, unique=True)

	class Meta:
		db_table = 'r_Media'
		verbose_name_plural = 'Media'

	def __unicode__(self):
		return self.title

	def get_absolute_url(self):
		if self.image:
			return "%s" % (self.image.url)
		else:
			return "%s" % (self.url)

	def save(self):
		if self.image:
			create_thumbnail(self)
		if not self.id:
			guid_base = str(uuid.uuid4())
			guid_encoded = guid_base.encode('ascii', 'ignore')
			guid = md5(guid_encoded).hexdigest()[:16]
			self.guid = guid
		super(Media, self).save()

class EntryType(models.Model):
	title = models.CharField(max_length=510)
	slug = models.SlugField(max_length=510, unique=True)
	guid = models.CharField(max_length=32, unique=True)
	user = models.ForeignKey(settings.AUTH_USER_MODEL)

	class Meta:
		db_table = 'r_EntryType'
		verbose_name_plural = 'Entry Types'
		ordering = ('-title',)

	def __unicode__(self):
		return self.title

	def entry_count(self):
		entry_total = Entry.objects.filter(post_type=self).count()
		return entry_total

	def save(self, *args, **kwargs):
		if not self.guid:
			#GUID Generation
			guid_base = str(uuid.uuid4())
			guid_encoded = guid_base.encode('ascii', 'ignore')
			guid = md5(guid_encoded).hexdigest()[:16]
			self.guid = guid
		super(EntryType, self).save(*args, **kwargs)

class Entry(models.Model):
	title = models.CharField(max_length=510)
	slug = models.SlugField(max_length=510, unique_for_date='pub_date')
	url = models.CharField(max_length=255, blank=True)
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	topic = models.ManyToManyField(Topic, db_table='r_Entry_Topics', blank=True)
	pub_date = models.DateTimeField(verbose_name=_("Publication date"), default=datetime.datetime.now)
	is_active = models.BooleanField(help_text=_("This should be checked for live entries"), choices=IS_ACTIVE_CHOICES, default=False)
	post_type = models.ForeignKey(EntryType, blank=True, null=True, default=1)
	content_format = models.CharField(choices=CONTENT_FORMAT_CHOICES, max_length=25, default='markdown')
	deck = models.TextField(_('deck'), blank=True)
	deck_html = models.TextField(blank=True)
	body = models.TextField(_('body'))
	body_html = models.TextField()
	image = models.ForeignKey(Media, blank=True, null=True)
	guid = models.CharField(max_length=32, unique=True)

	objects = EntryManager()

	class Meta:
		db_table = 'r_Entry'
		verbose_name_plural = 'entries'
		ordering = ('-pub_date',)
		get_latest_by = 'pub_date'
		unique_together = (('slug','user'),)

	def __unicode__(self):
		return self.title

	def Create_Draft(self):
		DraftInstance = Draft(
			entry=self,
			title=self.title,
			slug=self.slug,
			user=self.user,
			deck=self.deck,
			deck_html=self.deck_html,
			body=self.body,
			body_html=self.body_html,
			content_format=self.content_format
		)
		DraftInstance.save()
		return DraftInstance

	def get_absolute_url(self):
		if self.post_type.slug == 'page':
			return iri_to_uri(get_script_prefix().rstrip('/') + self.url)
		else:
			return "/%s/%s/" % (self.pub_date.strftime("%Y/%m").lower(), self.slug)

	def is_published(self):
		return self.is_active and self.pub_date <= datetime.datetime.now()
	is_published.boolean = True

	def save(self, *args, **kwargs):
		if self.id:
			self.Create_Draft()
		if not self.body:
			self.body = 'No text entered.'
			self.body_html = 'No text entered.'
		if not self.guid:
			#GUID Generation
			guid_base = "%s-%s-%s" % (self.user, self.pub_date, self.title)
			guid_encoded = guid_base.encode('ascii', 'ignore')
			guid = md5(guid_encoded).hexdigest()[:16]
			self.guid = guid
		if not self.pub_date:
			self.pub_date = datetime.datetime.now
		if self.content_format == u'markdown':
			self.deck_html = markdown.markdown(smart_unicode(self.deck))
			self.body_html = markdown.markdown(smart_unicode(self.body))
		else:
			self.body_html = self.body
			self.deck_html = self.deck
		if not self.title:
			self.title = guid
			self.slug = slugify(guid)
		self.slug = slugify(self.title)
		super(Entry, self).save(*args, **kwargs)

class Draft(models.Model):
	entry = models.ForeignKey(Entry)
	title = models.CharField(max_length=510, default='Untitled')
	last_edit = models.DateTimeField(verbose_name=_("Edit Date"), help_text=_("Last time draft was saved."), default=datetime.datetime.now)
	slug = models.SlugField(max_length=300, unique_for_date='pub_date')
	content_format = models.CharField(choices=CONTENT_FORMAT_CHOICES, max_length=25, default='markdown')
	deck = models.TextField(_('summary'), blank=True)
	deck_html = models.TextField(blank=True)
	body = models.TextField(_('body'))
	body_html = models.TextField()
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	guid = models.CharField(max_length=32, unique=True)

	class Meta:
		db_table = 'r_Draft'
		verbose_name_plural = 'drafts'
		ordering = ('-title',)
		get_latest_by = 'last_edit'

	def __unicode__(self):
		return self.title

	def save(self, *args, **kwargs):
		if not self.guid:
			#GUID Generation
			guid_base = "%s-%s-%s" % (str(uuid.uuid4()), self.user, self.last_edit)
			guid_encoded = guid_base.encode('ascii', 'ignore')
			guid = md5(guid_encoded).hexdigest()[:16]
			self.guid = guid

		if self.content_format == u'markdown':
			self.deck_html = markdown.markdown(smart_unicode(self.deck))
			self.body_html = markdown.markdown(smart_unicode(self.body))
		else:
			self.deck_html = self.deck
			self.body_html = self.body

		super(Draft, self).save(*args, **kwargs)


class ReadMore(models.Model):
	entry = models.ForeignKey(Entry)
	guid = models.CharField(max_length=32, unique=True)
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	pub_date = models.DateTimeField(verbose_name=_("Date Submitted"), default=datetime.datetime.now)
	url = models.URLField(max_length=255)
	title = models.CharField(max_length=510, default='Untitled')
	summary = models.TextField(_('summary'), blank=True)
	summary_html = models.TextField(blank=True)

	class Meta:
		db_table = 'r_ReadMore'
		verbose_name_plural = 'Entry Links'
		ordering = ('-title',)

	def __unicode__(self):
		return self.title

	def save(self, *args, **kwargs):
		if not self.guid:
			#GUID Generation
			guid_base = str(uuid.uuid4())
			guid_encoded = guid_base.encode('ascii', 'ignore')
			guid = md5(guid_encoded).hexdigest()[:16]
			self.guid = guid

		self.summary_html = markdown.markdown(smart_unicode(self.summary))
		super(ReadMore, self).save(*args, **kwargs)
