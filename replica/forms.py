from __future__ import absolute_import

import markdown
from django.utils.encoding import smart_unicode, smart_str
from django import forms
from django.forms import widgets
from .models import Entry

class EntryModelForm(forms.ModelForm):

	class Meta:
		model = Entry
		exclude = ('pub_date', 'slug', 'summary_html', 'body_html', 'author')
		widgets = {		
			'title': forms.TextInput(attrs={'class':'input-block-level', 'placeholder':'Title'}),
			'summary': forms.Textarea(attrs={'class':'input-block-level'}),
			'body': forms.Textarea(attrs={'class':'input-block-level'}),
			'is_active': forms.RadioSelect
		}

class SimpleEntryModelForm(forms.ModelForm):

	class Meta:
		model = Entry
		exclude = ('pub_date', 'slug', 'summary', 'summary_html', 'body_html', 'is_active', 'author')
		widgets = {		
			'title': forms.TextInput(attrs={'class':'input-block-level', 'placeholder':'Title'}),
			'body': forms.Textarea(attrs={'class':'input-block-level'}),
		}