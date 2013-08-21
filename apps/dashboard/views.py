from django.template import RequestContext
from django.shortcuts import render_to_response, render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.generic.dates import (ArchiveIndexView, YearArchiveView, MonthArchiveView, DayArchiveView, DateDetailView)
from django.views.generic.list import ListView

from wellplayed.apps.replica.models import Entry, Draft, Page, Media
from .forms import EntryModelForm, NanoEntryModelForm, DraftModelForm, PageModelForm

####Replica Admin
def ReplicaAdmin(request):
	
	published = Entry.objects.published().filter(author=request.user)
	ideas = Entry.objects.ideas().filter(author=request.user)
	upcoming = Entry.objects.upcoming().filter(author=request.user)
	pages = Page.objects.all()
	media = Media.objects.all()
		
	published_counts = {}
	for i in range(1,8):
		count = published.filter(pub_date__day=i).count()
		published_counts[i] = count
	
	chart_data = published_counts
	
	instance = Entry(author=request.user, is_active=False, post_type='article')
	f = NanoEntryModelForm(request.POST or None, instance=instance)
	if f.is_valid():
		f.save()
		messages.add_message(
			request, messages.INFO, 'Saved idea.')
		return redirect('replica-admin')

	ctx = {'form': f, 'published': published, 'ideas': ideas, 'upcoming': upcoming, 'pages': pages, 'media': media, 'chart_data': chart_data,}
	return render(request, 'dashboard/main.html', ctx)	

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
	variables = {'form': f, 'adding': True}
	return render(request, 'dashboard/create.html', variables)

def Replica_Nano(request):
	if request.method == "POST":
		instance = Entry(author=request.user)
		f = NanoEntryModelForm(request.POST or None, instance=instance)
		if f.is_valid():
			f.save()
			messages.add_message(
				request, messages.INFO, 'Entry Saved.')
			return redirect('replica-admin')
	else:
		initial = {}
		if "url" in request.GET:
			initial["url"] = request.GET["url"]
		if "title" in request.GET:
			initial["title"] = request.GET["title"].strip()
		if initial:
			f = NanoEntryModelForm(initial=initial)
		else:
			f = NanoEntryModelForm()
				
	variables = {'form': f, 'adding': True}
	return render(request, 'dashboard/nano.html', variables)

def ReplicaDelete(request, entry_id):
	entry = get_object_or_404(Entry, pk=entry_id, author=request.user)
	if request.method == 'POST':
		entry.delete()
		return redirect('replica-admin')
	return render(request, 'dashboard/delete-confirm.html', {'entry': entry})

def ReplicaEdit(request, entry_id):
	entry = get_object_or_404(Entry, pk=entry_id, author=request.user)
	f = EntryModelForm(request.POST or None, instance=entry)
	if f.is_valid():
		f.save()
		messages.add_message(
			request, messages.INFO, 'Entry Saved.')
		return redirect('replica-edit', entry_id=entry_id)
	variables = RequestContext(request, {'form': f, 'entry': entry, 'adding': False})
	return render_to_response('dashboard/create.html', variables)

def ReplicaDrafts(request, entry_id):
	entry = get_object_or_404(Entry, pk=entry_id, author=request.user)
	drafts = Draft.objects.all().filter(entry=entry, author=request.user)
	variables = RequestContext(request, {'entry': entry, 'drafts': drafts,})
	return render_to_response('dashboard/drafts.html', variables)
	
def ReplicaDraftsView(request, entry_id, draft_id):
	entry = get_object_or_404(Entry, pk=entry_id, author=request.user)
	draft = get_object_or_404(Draft, pk=draft_id, author=request.user)
	f = DraftModelForm(request.POST or None, instance=draft)
	if f.is_valid():
		f.save()
		messages.add_message(
			request, messages.INFO, 'Draft edited.')
		return redirect('replica-admin')
	variables = RequestContext(request, {'form': f, 'entry': entry, 'draft': draft,})
	return render_to_response('dashboard/drafts_view.html', variables)
	
def ReplicaDraftDelete(request, draft_id):
	entry = get_object_or_404(Draft, pk=draft_id, author=request.user)
	if request.method == 'POST':
		entry.delete()
		messages.add_message(
			request, messages.INFO, 'Draft deleted.')
		return redirect('replica-admin')
	return render(request, 'dashboard/delete-confirm.html', {'entry': entry})

class ReplicaAdminViewMixin(object):

	date_field = 'pub_date'
	paginate_by = 15
	allow_empty = True
	month_format = "%m"

	def get_queryset(self):
		return Entry.objects.published().filter(author=self.request.user)

class ReplicaAdminArchiveIndexView(ReplicaAdminViewMixin, ArchiveIndexView):
    pass

class ReplicaAdminYearArchiveView(ReplicaAdminViewMixin, YearArchiveView):
    pass

class ReplicaAdminMonthArchiveView(ReplicaAdminViewMixin, MonthArchiveView):
    pass

class ReplicaAdminDayArchiveView(ReplicaAdminViewMixin, DayArchiveView):
    pass


class ReplicaPageListView(ListView):
	paginate_by = 5
	template_name = 'dashboard/page_list.html'
	
	def get_queryset(self):
		self.published = Page.objects.all()[5:25]
		return Page.objects.order_by('-pub_date')

	def get_context_data(self, **kwargs):
		context = super(ReplicaPageListView, self).get_context_data(**kwargs)
		context.update({'published': self.published,})
		return context

def ReplicaPage(request):
	instance = Page()
	f = PageModelForm(request.POST or None, instance=instance)
	if f.is_valid():
		f.save()
		messages.add_message(
			request, messages.INFO, 'Entry Created.')
		return redirect('replica-admin')
	variables = {'form': f, 'adding': True}
	return render(request, 'dashboard/page.html', variables)

def ReplicaPageEdit(request, page_id):
	page = get_object_or_404(Page, pk=page_id)
	f = PageModelForm(request.POST or None, instance=page)
	if f.is_valid():
		f.save()
		messages.add_message(
			request, messages.INFO, 'Page edited.')
		return redirect('replica-admin')
	variables = RequestContext(request, {'form': f, 'page': page, 'adding': False})
	return render_to_response('dashboard/page.html', variables)