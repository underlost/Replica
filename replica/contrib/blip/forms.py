from __future__ import absolute_import

import markdown
from django.utils.encoding import smart_unicode, smart_str
from django import forms
from django.forms import widgets
from .models import Timeline, Blip


class TimelineModelForm(forms.ModelForm):

	class Meta:
		model = Timeline
		exclude = ('pub_date', 'slug', 'user', 'image', 'guid',)
		widgets = {
			'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Title'}),
		}


class BlipModelForm(forms.ModelForm):

	class Meta:
		model = Blip
		exclude = ('pub_date', 'timeline', 'user', 'body_html', 'guid')
		widgets = {
			'body': forms.Textarea(attrs={'class':'form-control', 'rows':'2', 'placeholder':'Start typing something...'}),
		}
