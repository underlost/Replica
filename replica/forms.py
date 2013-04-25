from __future__ import absolute_import

import markdown
from django.utils.encoding import smart_unicode, smart_str
from django import forms
from django.forms import widgets
from .models import Entry, Draft

class EntryModelForm(forms.ModelForm):

	class Meta:
		model = Entry
		exclude = ('pub_date', 'slug', 'summary_html', 'body_html', 'author')
		widgets = {		
			'title': forms.TextInput(attrs={'class':'input-block-level', 'placeholder':'Title'}),
			'summary': forms.Textarea(attrs={'class':'input-block-level'}),
			'body': forms.Textarea(attrs={'class':'input-block-level', 'placeholder':'Start typing'}),
			'is_active': forms.RadioSelect
		}

class NanoEntryModelForm(forms.ModelForm):

	class Meta:
		model = Entry
		exclude = ('pub_date', 'slug', 'summary_html', 'body_html', 'author')
		widgets = {		
			'title': forms.TextInput(attrs={'class':'input-block-level', 'placeholder':'Title'}),
			'body': forms.Textarea(attrs={'class':'input-block-level', 'placeholder':'Start typing'}),
		}
		
class DraftModelForm(forms.ModelForm):

	class Meta:
		model = Draft
		exclude = ('last_edit', 'slug', 'summary_html', 'body_html', 'author')