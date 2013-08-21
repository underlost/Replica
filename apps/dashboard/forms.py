from __future__ import absolute_import

import markdown
from django.utils.encoding import smart_unicode, smart_str
from django import forms
from django.forms import widgets, Select

from wellplayed.apps.replica.models import Entry, Draft, Page

class EntryModelForm(forms.ModelForm):

	class Meta:
		model = Entry
		exclude = ('pub_date', 'slug', 'summary_html', 'body_html', 'author')
		widgets = {		
			'title': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Title', 'value':''}),
			'summary': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Optional Summary'}),
			'url': forms.TextInput(attrs={'class':'form-control', 'placeholder':'URL',}),
			'body': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Start typing', 'data-provide':'markdown'}),
			'is_active': forms.RadioSelect
		}

class NanoEntryModelForm(forms.ModelForm):

	class Meta:
		model = Entry
		exclude = ('pub_date', 'slug', 'summary_html', 'body_html', 'author')
		widgets = {		
			'title': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Title', 'value':''}),
			'url': forms.TextInput(attrs={'class':'form-control', 'placeholder':'URL',}),
			'body': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Start typing', 'data-provide':'markdown'}),
			'summary': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Optional Summary'}),
			
			'post_type': forms.Select(attrs={'class':'form-control',}),
			'content_format': forms.Select(attrs={'class':'form-control',}),
			
			'is_active': forms.RadioSelect
		}

class DraftModelForm(forms.ModelForm):

	class Meta:
		model = Draft
		exclude = ('last_edit', 'slug', 'summary_html', 'body_html', 'author')


class PageModelForm(forms.ModelForm):

	class Meta:
		model = Page
		exclude = ('pub_date', 'description_html', 'content_html')
		widgets = {		
			'title': forms.TextInput(attrs={'class':'form-control', 'placeholder':'New Page', 'value':''}),
			'content': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Start typing'}),
			'description': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Start typing'}),
		}