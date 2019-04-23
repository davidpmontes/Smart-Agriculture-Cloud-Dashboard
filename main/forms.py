from django import forms

class NetworkCreationForm(forms.Form):
	networkName = forms.CharField(label='Network name', max_length=100)
	lat = forms.CharField(label='Latitude', max_length=100)
	lon = forms.CharField(label='Longitude', max_length=100)

	class Meta:
		fields = ['your_name']

class NetworkDeletionForm(forms.Form):

	class Meta:
		fields = ['your_name']