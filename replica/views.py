from django.template import RequestContext
from django.shortcuts import render_to_response, render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.generic.dates import (ArchiveIndexView, YearArchiveView, MonthArchiveView, DayArchiveView)

from .models import Entry, Page
from .forms import EntryModelForm

class ReplicaViewMixin(object):

	date_field = 'pub_date'
	paginate_by = 10
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

def entry_detail(request, slug):
	entry = get_object_or_404(Entry, slug=slug)
	variables = RequestContext(request, {'object': entry})
	return render_to_response(['replica/articles/%s.html' % entry.slug, 'replica/entry_detail.html'], variables)

####Pages
def Index(request):
	objects = Entry.objects.published()[:10]
	variables = RequestContext(request, {'objects': objects,})
	return render_to_response('replica/entry_index.html', variables)

def page(request, slug):
	page = get_object_or_404(Page, slug=slug)
	variables = RequestContext(request, {'object': page})
	return render_to_response(['replica/pages/%s.html' % page.slug, 'replica/page.html'], variables)

####Replica Admin
@login_required
def ReplicaAdmin(request):
	published = Entry.objects.published().filter(author=request.user)
	ideas = Entry.objects.ideas().filter(author=request.user)
	variables = RequestContext(request, {'published': published, 'ideas': ideas,})
	return render_to_response('replica/admin/main.html', variables)

@login_required
def ReplicaCreate(request):

	if request.method == "POST":
		instance = Entry(author=request.user)
		f = EntryModelForm(request.POST or None, instance=instance)
		if f.is_valid():
			f.save()
			messages.add_message(
				request, messages.INFO, 'Entry Created.')
			return redirect('replica-admin')
	else:
		initial = {}
		if "url" in request.GET:
			initial["url"] = request.GET["url"]
		if "title" in request.GET:
			initial["title"] = request.GET["title"].strip()
		if initial:
			f = EntryModelForm(initial=initial)
		else:
			f = EntryModelForm()
			
	entry_add_url = "http://" + Site.objects.get_current().domain + reverse(ReplicaCreate)
	#bookmarklet = "javascript:window.location.href='%s?url=%22+encodeURIComponent(document.location)+%22&title=%22+encodeURIComponent(document.title)'" % entry_add_url
	bookmarklet = "javascript:window.location=%22http://underlost.net/replicate/create/?url=%22+encodeURIComponent(document.location)+%22&title=%22+encodeURIComponent(document.title)"
	variables = {'form': f, "bookmarklet": bookmarklet, 'adding': True}
	return render(request, 'replica/admin/create.html', variables)

@login_required
def ReplicaDelete(request, entry_id):
	entry = get_object_or_404(Entry, pk=entry_id, author=request.user)
	if request.method == 'POST':
		entry.delete()
		return redirect('replica-admin')
	return render(request, 'replica/admin/delete-confirm.html', {'entry': entry})

@login_required
def ReplicaEdit(request, entry_id):
	entry = get_object_or_404(Entry, pk=entry_id, author=request.user)
	f = EntryModelForm(request.POST or None, instance=entry)
	if f.is_valid():
		f.save()
		return redirect('replica-admin')
	variables = RequestContext(request, {'form': f, 'entry': entry, 'adding': False})
	return render_to_response('replica/admin/create.html', variables)