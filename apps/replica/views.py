from django.template import RequestContext
from django.shortcuts import render_to_response, render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.generic.dates import (ArchiveIndexView, YearArchiveView, MonthArchiveView, DayArchiveView, DateDetailView)
from django.views.generic.list import ListView

from .models import Entry, Draft, Page
from .forms import EntryModelForm, NanoEntryModelForm, DraftModelForm

class ReplicaViewMixin(object):

	date_field = 'pub_date'
	paginate_by = 15
	allow_empty = True
	month_format = "%m"

	def get_allow_future(self):
		return self.request.user.is_staff

	def get_queryset(self):
		if self.request.user.is_staff:
			return Entry.objects.all()
		else:
			return Entry.objects.published()

class ReplicaArchiveIndexView(ReplicaViewMixin, ArchiveIndexView):
    pass

class ReplicaYearArchiveView(ReplicaViewMixin, YearArchiveView):
    pass

class ReplicaMonthArchiveView(ReplicaViewMixin, MonthArchiveView):
    pass

class ReplicaDayArchiveView(ReplicaViewMixin, DayArchiveView):
    pass

class ReplicaDateDetailView(ReplicaViewMixin, DateDetailView):
    pass

def ReplicaEntryFeatured(request, slug):
	entry = get_object_or_404(Entry, slug=slug, post_type='featured')
	variables = RequestContext(request, {'object': entry})
	return render_to_response(['replica/articles/%s.html' % entry.slug, 'replica/entry_detail.html'], variables)
	

class PagesListView(ListView):
	paginate_by = 10
	#template_name = 'replica/page_list.html'
	
	def get_queryset(self):
		if self.request.user.is_staff:
			return Page.objects.all()
		else:
			return Page.objects.published()

	def get_context_data(self, **kwargs):
		context = super(PagesListView, self).get_context_data(**kwargs)
		return context