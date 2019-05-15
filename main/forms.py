from django import forms
import requests

FARM_TYPES = (
    ('Cherry', 'Cherry'),
    ('Pickles', 'Pickles'),
    ('Strawberry', 'Strawberry')
)

SENSOR_TYPES = (
    ('Water', 'Water'),
    ('Temperature', 'Temperature'),
    ('PH', 'PH')
)

STATUS_TYPES = (
    ('Active', 'Active'),
    ('Inactive', 'Inactive')
)

url = "http://ec2-3-81-127-12.compute-1.amazonaws.com:8080/"


class SensorForm(forms.Form):
	sensorID = forms.CharField(label='Sensor ID', max_length=100)
	sensorType = forms.ChoiceField(label='Farm type', choices=SENSOR_TYPES)
	status = forms.ChoiceField(label='Farm type', choices=STATUS_TYPES)

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

class FarmEditForm(forms.Form):
	allNetworkID = []

	networkID = forms.ChoiceField(label='Network ID')
	name = forms.CharField(label='Farm name', max_length=100)
	farmType = forms.ChoiceField(label='Farm type', choices=FARM_TYPES)
	userID = forms.CharField(label='Username', max_length=100)
	lat = forms.CharField(label='Latitude', max_length=100)
	lon = forms.CharField(label='Longitude', max_length=100)

	def __init__(self, *args, **kwargs):
		super(FarmEditForm, self).__init__(*args, **kwargs)
		self.allNetworkID = []
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

class SensorNodeDeletionForm(forms.Form):

	class Meta:
		fields = ['your_name']


class ClusterNodeDeletionForm(forms.Form):

	class Meta:
		fields = ['your_name']
