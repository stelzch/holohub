from django import forms

class ProjectForm(forms.Form):
	title = forms.CharField(label='Title', max_length=255)
	description = forms.CharField(label='Description', max_length=10000)
	projectfile = forms.FileField(label='Project file')
