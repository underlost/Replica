from __future__ import absolute_import

import markdown
from django.utils.encoding import smart_unicode, smart_str
from django import forms
from django.utils.safestring import mark_safe
from django.forms import widgets, Select
from django.forms.fields import DateField
from django.db.models import Q

from core.models import Account
from .models import Entry, Media, Draft, Topic, EntryType
from .widgets import DateTimeWidget

dateTimeOptions = {
	'format': 'dd/mm/yyyy HH:ii P',
	'autoclose': 'true',
	'showMeridian' : 'true'
}

class CheckboxSelectMultipleP(forms.CheckboxSelectMultiple):
	def render(self, *args, **kwargs):
		output = super(CheckboxSelectMultipleP, self).render(*args,**kwargs)
		return mark_safe(output.replace(u'<ul>', u'').replace(u'</ul>', u'').replace(u'<li>', u'<div class="col-md-2">').replace(u'</li>', u'</div>'))

class EntryModelForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super(EntryModelForm, self).__init__(*args, **kwargs)
		self.user = kwargs.get('instance').user
		self.fields['image'].queryset = Media.objects.filter(user=self.user)
		self.fields['topic'].queryset = Topic.objects.filter(
			Q(user=self.user) |
			Q(members=self.user)
		)

	class Meta:
		model = Entry
		exclude = ('slug', 'deck_html', 'body_html', 'user', 'guid', 'content_format', )
		widgets = {
			'title': forms.Textarea(attrs={'class':'form-control ReplicaForm nano_title', 'placeholder':'Title', 'rows':'1', 'value':''}),
			'deck': forms.Textarea(attrs={'class':'form-control ReplicaForm nano_deck', 'placeholder':'Optional Summary', 'rows':'1'}),
			'pub_date': forms.TextInput(attrs={'id': 'datetimepicker', 'class':'form-control', 'placeholder':'Publish Date', 'data-date-format': 'yyyy-mm-dd hh:ii' }),
			'url': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Link to another url?',}),
			'body': forms.Textarea(attrs={'class':'form-control ReplicaForm', 'placeholder':'Start typing', 'data-provide':'markdown'}),
			'is_active': forms.RadioSelect,
			'topic': forms.CheckboxSelectMultiple(),
			'post_type': forms.Select(attrs={'class':'form-control',}),
			'image': forms.Select(attrs={'class':'form-control',}),
		}

class QuickEntryModelForm(forms.ModelForm):

	title = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control ReplicaForm nano_title', 'placeholder':'Optional Title', 'value':''}))
	body = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control ReplicaForm', 'placeholder':'Just start typing...', 'rows':'1',}))

	class Meta:
		model = Entry
		exclude = ('slug', 'deck_html', 'body_html', 'user', 'guid', 'image','content_format', 'post_type', 'Topic', 'deck',)
		widgets = {
			'url': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Link to another url?',}),
			'pub_date': forms.TextInput(attrs={'id': 'datetimepicker', 'class':'form-control', 'placeholder':'Publish Date', 'data-date-format': 'yyyy-mm-dd hh:ii' }),
			'is_active': forms.RadioSelect,
		}

class DraftModelForm(forms.ModelForm):

	class Meta:
		model = Draft
		exclude = ('last_edit', 'slug', 'deck_html', 'body_html', 'user')


class TopicModelForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super(TopicModelForm, self).__init__(*args, **kwargs)
		self.fields['members'].queryset = Account.objects.filter(is_staff=True)

	class Meta:
		model = Topic
		exclude = ('pub_date', 'slug', 'user', 'guid', 'thumbnail',)
		widgets = {
			'title': forms.TextInput(attrs={'class':'form-control ReplicaForm nano_title', 'placeholder':'Topic name',}),
			'description': forms.Textarea(attrs={'class':'form-control ReplicaForm', 'placeholder':'Describe your topic', 'rows':'1'}),
			'is_public': forms.RadioSelect,
			'members': CheckboxSelectMultipleP(),
			'image': forms.ClearableFileInput,

		}

class EntryTypeModelForm(forms.ModelForm):

	title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control ReplicaForm', 'placeholder':'Entry Type Name', 'value':''}))
	slug = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control ReplicaForm', 'placeholder':'Entry Type Name', 'value':''}))

	class Meta:
		model = EntryType
		exclude = ('user', 'guid',)


class MediaModelForm(forms.ModelForm):

	class Meta:
		model = Media
		exclude = ('pub_date', 'user', 'guid', 'thumbnail',)
		widgets = {
			'title': forms.TextInput(attrs={'class':'form-control ReplicaForm', 'placeholder':'Image Title',}),
			'description': forms.Textarea(attrs={'class':'form-control ReplicaForm', 'placeholder':'Brief media description', 'rows':'1'}),
			'url': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Link to an image?',}),
			'image': forms.ClearableFileInput,

		}
