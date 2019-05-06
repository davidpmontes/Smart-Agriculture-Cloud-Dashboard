from django import forms
import requests


url = "http://ec2-3-81-30-51.compute-1.amazonaws.com:8080/"


class SensorForm(forms.Form):
	SensorID = forms.CharField(label='SensorID', max_length=100)
	SensorNodeID = forms.CharField(label='SensorNodeID', max_length=100)
	Type = forms.CharField(label='Type', max_length=100)
	Status = forms.CharField(label='Status', max_length=100)

	class Meta:
		fields = ['your_name']

class SensorNodeForm(forms.Form):
	lat = forms.CharField(label='Latitude', max_length=100)
	lon = forms.CharField(label='Longitude', max_length=100)

	class Meta:
		fields = ['your_name']

class ClusterNodeForm(forms.Form):
	lat = forms.CharField(label='Latitude', max_length=100)
	lon = forms.CharField(label='Longitude', max_length=100)

	class Meta:
		fields = ['your_name']

FARM_TYPES = (
	('Cherry', 'Cherry'),
    ('Pickles','Pickles'),
    ('Strawberry','Strawberry')
)

class FarmEditForm(forms.Form):
	allNetworkID = []

	networkID = forms.ChoiceField(label='Network ID')
	name = forms.CharField(label='Farm name', max_length=100)
	farmType = forms.ChoiceField(label='Farm type', choices=FARM_TYPES)
	userID = forms.CharField(label='Users email address', max_length=100)
	lat = forms.CharField(label='Latitude', max_length=100)
	lon = forms.CharField(label='Longitude', max_length=100)

	def __init__(self, *args, **kwargs):
		super(FarmEditForm, self).__init__(*args, **kwargs)
		try:
			getAllNetworkID = requests.get(url = url + "getAllNetwork").json()
			for n in getAllNetworkID:
	 			self.allNetworkID.append((n['networkID'], n['networkID']))
		except:
			 print("error")
		self.fields['networkID'] = forms.ChoiceField(label='Network ID', choices=self.allNetworkID)


	class Meta:
		fields = ['your_name']

class NetworkCreationForm(forms.Form):
	networkName = forms.CharField(label='Network name', max_length=100)
	lat = forms.CharField(label='Latitude', max_length=100)
	lon = forms.CharField(label='Longitude', max_length=100)

	class Meta:
		fields = ['your_name']

class NetworkDeletionForm(forms.Form):

	class Meta:
		fields = ['your_name']

class SensorDeletionForm(forms.Form):

	class Meta:
		fields = ['your_name']