import datetime
import markdown

from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

class TopicManager(models.Manager):

	def open(self):
		return self.public().filter(pub_date__lte=datetime.datetime.now()).filter(can_submit=True)

	def public(self):
		return super(TopicManager, self).get_query_set().filter(is_public=True)

	def mine(self, user):
		return super(TopicManager, self).get_query_set().filter(
			Q(user=user) |
			Q(members=user)
		)

class EntryManager(models.Manager):

	def published(self):
		return self.active().filter(pub_date__lte=datetime.datetime.now())

	def upcoming(self):
		return self.active().filter(pub_date__gte=datetime.datetime.now())

	def ideas(self):
		return super(EntryManager, self).get_query_set().filter(is_active=False)

	def active(self):
		return super(EntryManager, self).get_query_set().filter(is_active=True)
