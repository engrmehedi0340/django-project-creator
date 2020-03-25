from django import forms


class DjangoFieldForm(forms.Form):
	project_name = forms.CharField(max_length = 200, widget=forms.TextInput(
	                    attrs={'placeholder': 'Enter project name '}))
	app_name = forms.CharField(max_length=200, widget=forms.TextInput(
	                    attrs={'placeholder': 'Enter application name'}))
	