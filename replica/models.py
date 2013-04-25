import datetime
import markdown

import os
import urllib2
from urlparse import urlparse
from cStringIO import StringIO
from PIL import Image

from django.conf import settings
from django.db import models
from django.contrib.sites.models import Site
from django.contrib.flatpages.models import FlatPage
from django.contrib.auth.models import User
from django.utils.encoding import smart_unicode, smart_str
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from django.core.files.uploadedfile import SimpleUploadedFile

class EntryManager(models.Manager):
	
	def published(self):
		return self.active().filter(pub_date__lte=datetime.datetime.now())
	
	def ideas(self):
		return super(EntryManager, self).get_query_set().filter(is_active=False)
	
	def active(self):
		return super(EntryManager, self).get_query_set().filter(is_active=True)

CONTENT_FORMAT_CHOICES = (
	(u'markdown', u'Markdown'),
	(u'html', u'Raw HTML'),
)

POST_TYPE_CHOICES = (
	(u'articles', u'Article'),
	(u'aside', u'Aside'),
	(u'linked', u'Link'),
	(u'image', u'Image'),	
	(u'video', u'Video'),
	(u'code', u'Code'),	
)

IS_ACTIVE_CHOICES = ((True, 'Published'), (False, 'Draft'))

def upload_original(instance, filename):
	return 'media/images/original/%s/%s' % (instance.user.id, filename)

def upload_thumb(instance, filename):
	return 'media/images/thumbnail/300/%s/%s' % (instance.user.id, filename)

class Media(models.Model):
	title = models.CharField(max_length=200)
	pub_date = models.DateTimeField(auto_now_add=True)
	description = models.CharField(max_length=500, blank=True)
	url = models.URLField(unique=True, blank=True)
	image = models.ImageField(upload_to=upload_original, blank=True, null=True)
	thumbnail = models.ImageField(upload_to=upload_thumb, blank=True, null=True)
	user = models.ForeignKey(User, blank=True)

	class Meta:
		db_table = 'replica_media'
		verbose_name_plural = 'Media'
		
	def __unicode__(self):
		return self.title
   
	def get_absolute_url(self):
		if self.image:
			return "%s" % (self.image.url)
		else:	
			return "%s" % (self.url)
	
	def create_thumbnail(self, content_type=None):
		if not self.image:
			return
		THUMBNAIL_SIZE = (300, 2500)
		DJANGO_TYPE = content_type if content_type else self.image.file.content_type

		if DJANGO_TYPE == 'image/jpeg':
			PIL_TYPE = 'jpeg'
			FILE_EXTENSION = 'jpg'
		elif DJANGO_TYPE == 'image/png':
			PIL_TYPE = 'png'
			FILE_EXTENSION = 'png'

		image = Image.open(StringIO(self.image.read()))
		image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)
		temp_handle = StringIO()
		image.save(temp_handle, PIL_TYPE)
		temp_handle.seek(0)
		suf = SimpleUploadedFile(os.path.split(self.image.name)[-1],
				temp_handle.read(), content_type=DJANGO_TYPE)
		self.thumbnail.save('%s_thumbnail.%s'%(os.path.splitext(suf.name)[0],FILE_EXTENSION), suf, save=False)
	
	def save(self):
		self.create_thumbnail()
		super(Media, self).save()
	
class Entry(models.Model):
	title = models.CharField(max_length=200, default='Untitled Post')
	url = models.URLField(blank=True)
	slug = models.SlugField(unique_for_date='pub_date')
	post_type = models.CharField(choices=POST_TYPE_CHOICES, max_length=10, default='articles')
	is_active = models.BooleanField(help_text=_("This should be checked for live entries."), choices=IS_ACTIVE_CHOICES, default=False)
	pub_date = models.DateTimeField(verbose_name=_("Publication date"), help_text=_("Entries set to a future date will only be visible for admin."), default=datetime.datetime.now)
	image = models.ForeignKey(Media, blank=True, null=True)
	content_format = models.CharField(choices=CONTENT_FORMAT_CHOICES, max_length=25, default='markdown')
	summary = models.TextField(_('summary'), blank=True)
	summary_html = models.TextField(blank=True)
	body = models.TextField(_('body'))
	body_html = models.TextField()
	author = models.ForeignKey(User, blank=True)

	objects = EntryManager()
	
	class Meta:
		db_table = 'replica_entries'
		verbose_name_plural = 'entries'
		ordering = ('-pub_date',)
		get_latest_by = 'pub_date'

	def __unicode__(self):
		return self.title

	def Create_Draft(self):
	    DraftInstance = Draft(entry=self, title=self.title, slug=self.slug, author=self.author, summary=self.summary, summary_html=self.summary_html, body=self.body, body_html=self.body_html, content_format=self.content_format)
	    DraftInstance.save()
	    return DraftInstance
	
	def get_absolute_url(self):
		return "/blog/%s/" % (self.slug)
			
	def is_published(self):
		return self.is_active and self.pub_date <= datetime.datetime.now()
	is_published.boolean = True

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = slugify(self.title)
			
		if self.content_format == u'markdown':
			self.summary_html = markdown.markdown(smart_unicode(self.summary))
			self.body_html = markdown.markdown(smart_unicode(self.body))
		else:	
			self.summary_html = self.summary
			self.body_html = self.body 			
		
		self.Create_Draft()
		super(Entry, self).save(*args, **kwargs)

class Draft(models.Model):
	entry = models.ForeignKey(Entry)
	title = models.CharField(max_length=200, default='Untitled Post')
	last_edit = models.DateTimeField(verbose_name=_("Edit Date"), help_text=_("Last time draft was saved."), auto_now_add=True)
	slug = models.SlugField(unique_for_date='pub_date')
	content_format = models.CharField(choices=CONTENT_FORMAT_CHOICES, max_length=25, default='markdown')
	summary = models.TextField(_('summary'), blank=True)
	summary_html = models.TextField(blank=True)
	body = models.TextField(_('body'))
	body_html = models.TextField()
	author = models.ForeignKey(User, blank=True)
	
	class Meta:
		db_table = 'replica_drafts'
		verbose_name_plural = 'drafts'
		ordering = ('-title',)
		get_latest_by = 'last_edit'

	def __unicode__(self):
		return self.title
	
	def save(self, *args, **kwargs):			
		if self.content_format == u'markdown':
			self.summary_html = markdown.markdown(smart_unicode(self.summary))
			self.body_html = markdown.markdown(smart_unicode(self.body))
		else:	
			self.summary_html = self.summary
			self.body_html = self.body
						
		super(Draft, self).save(*args, **kwargs)

class Page(FlatPage):
	is_active = models.BooleanField(help_text=_("This should be checked for live Pages."), default=False)
	pub_date = models.DateTimeField(verbose_name=_("Publication date"), help_text=_("Pages set to a future date will only be visible for admin."), auto_now_add=True)
	content_format = models.CharField(choices=CONTENT_FORMAT_CHOICES, max_length=25)
	description = models.TextField(_('description'), blank=True)
	description_html = models.TextField(blank=True)
	content_html = models.TextField()
	
	objects = EntryManager()

	def is_published(self):
		return self.is_active and self.pub_date <= datetime.datetime.now()
	is_published.boolean = True

	def save(self, *args, **kwargs):					
		if self.content_format == u'html':
			self.description_html = self.description
			self.content_html = self.content       
		elif self.content_format == u'markdown':
			self.description_html = markdown.markdown(smart_unicode(self.description))
			self.content_html = markdown.markdown(smart_unicode(self.content))
		
		super(Page, self).save(*args, **kwargs)