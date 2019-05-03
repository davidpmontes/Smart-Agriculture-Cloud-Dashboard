from django.shortcuts import render, redirect
from django.contrib import messages
from requests.exceptions import ConnectionError
from . forms import NetworkCreationForm, NetworkDeletionForm, FarmEditForm, SensorNodeForm, ClusterNodeForm, SensorForm, SensorDeletionForm
import requests
import urllib.parse

url = "http://ec2-54-197-218-120.compute-1.amazonaws.com:8080"


def editFarm(request, farmid=''):
	if request.method == 'POST':
		form = FarmEditForm(request.POST)
		if form.is_valid():
			messages.success(request, f'Farm updated!')
			return redirect('main-home')
	else:
		form = FarmEditForm()

	return render(request, 'main/editFarm.html', {'form': form, 'farmid': farmid})

def addSensor(request, sensornodeid=''):
	if request.method == 'POST':
		form = SensorForm(request.POST)
		if form.is_valid():
			messages.success(request, f'Your new Sensor has been created!')
			return redirect('main-home')
	else:
		form = SensorForm()

	return render(request, 'main/addSensor.html', {'form': form, 'sensornodeid': sensornodeid})


def addSensorNode(request, farmname='', farmid=''):
	if request.method == 'POST':
		form = SensorNodeForm(request.POST)
		if form.is_valid():
			messages.success(request, f'New Sensor Node created!')
			return redirect('main-adminmapdetails', farmname=farmname, farmid=farmid)
	else:
		form = SensorNodeForm()

	return render(request, 'main/addSensorNode.html', {'form': form, 'farmid': farmid})

def addClusterNode(request, farmname='', farmid=''):
	if request.method == 'POST':
		form = ClusterNodeForm(request.POST)
		if form.is_valid():
			messages.success(request, f'New Cluster Node created!')
			return redirect('main-adminmapdetails', farmname=farmname, farmid=farmid)

	else:
		form = ClusterNodeForm()

	return render(request, 'main/addClusterNode.html', {'form': form, 'farmid': farmid})

def allfarmersmaps(request, username=''):
	displayInfo = GetFarms(request)
	return render(request, 'main/allfarmersmaps.html', {"displayInfo": displayInfo})

def farmermapdetails(request, farmname='', farmid=''):
	displayInfo = GetFarmNodes(farmname)
	return render(request, 'main/farmermapdetails.html', {"farmname": farmname, "farmid": farmid, "displayInfo": displayInfo})

def adminmapdetails(request, farmname='', farmid=''):
	displayInfo = GetFarmNodes(farmname)
	return render(request, 'main/adminmapdetails.html', {"farmname": farmname, "farmid": farmid, "displayInfo": displayInfo})

def allfarms(request, networkname=''):
	return render(request, 'main/allfarms.html', {"networkname": networkname})

def allnetworks(request):
	response = requests.get(urllib.parse.urljoin(url, "getAllNetwork"))
	results = response.json()
	print(results)
	return render(request, 'main/allnetworks.html', {"results": results})

def deleteSensor(request, sensorid=''):
	if request.method == 'POST':
		form = SensorDeletionForm(request.POST)
		if form.is_valid():
			messages.success(request, f'Sensor deleted')
			return redirect('main-home')
	else:
		form = SensorDeletionForm()

	return render(request, 'main/deleteSensor.html', {'form': form, 'sensorid': sensorid})

def deleteNetwork(request):
	if request.method == 'POST':
		form = NetworkDeletionForm(request.POST)
		if form.is_valid():
			#api call to delete NewNetwork
			messages.success(request, f'Network has been deleted')
			return redirect('main-home')
	else:
		form = NetworkDeletionForm()

	return render(request, 'main/deleteNetwork.html', {'form': form})


def createNetwork(request):
	if request.method == 'POST':
		form = NetworkCreationForm(request.POST)
		if form.is_valid():
			#api call to get NetworkNames
			existingNetworkNames = ['farm1', 'farm2']

			if form.cleaned_data.get('networkName') in existingNetworkNames:
				messages.error(request, f'That network name already exists')
			else:
				#api call to create NewNetwork
				messages.success(request, f'Your new network has been created!')
				return redirect('main-home')
	else:
		form = NetworkCreationForm()

	return render(request, 'main/createNetwork.html', {'form': form})



def home(request, id=''):	
	return render(request, 'main/home.html')

def GetFarms(request):
	value = {}
	username = request.user.username

	if username=="davidpmontes":
		value = {
			"Farms": [{
				"ID": 123,
				"Name": "MilpitasFarm",
				"Type": "Apple",
				"Lat": 37.431315,
				"Lon": -121.945802
			}, {
				"ID": 456,
				"Name": "WestFarm",
				"Type": "Strawberry",
				"Lat": 37.302925,
				"Lon": -122.019987
			}, {
				"ID": 789,
				"Name": "AndersonLakeFarm",
				"Type": "Watermelon",
				"Lat": 37.191506,
				"Lon": -121.609035
			}]
		}
	elif username=="johndoe":
		value = {
			"Farms": [{
				"ID": 123,
				"Name": "MilpitasFarm",
				"Type": "Apple",
				"Lat": 37.431315,
				"Lon": -121.945802
			}]
		}
	return value

def GetFarmNodes(farmname):
	if farmname=="WestFarm":
		value = {
			"ClusterNodes": [{
				"ID": 123,
				"Status": "Active",
				"Lat": 35.51,
				"Lon": -120.51,
				"SensorNodes": [{
						"ID": 1,
						"Status": "Active",
						"Lat": 35.52,
						"Lon": -120.51
					}, {
						"ID": 2,
						"Status": "Active",
						"Lat": 35.51,
						"Lon": -120.5
					},
					{
						"ID": 3,
						"Status": "InActive",
						"Lat": 35.5,
						"Lon": -120.5
					}
				]
			}, {
				"ID": 456,
				"Status": "Active",
				"Lat": 35.42,
				"Lon": -120.42,
				"SensorNodes": [{
						"ID": 4,
						"Status": "Active",
						"Lat": 35.42,
						"Lon": -120.4
					}, {
						"ID": 5,
						"Status": "Active",
						"Lat": 35.42,
						"Lon": -120.44
					},
					{
						"ID": 6,
						"Status": "Active",
						"Lat": 35.41,
						"Lon": -120.42
					}
				]
			}]
		}
	elif farmname=="MilpitasFarm":
		value = {
			"ClusterNodes": [{
				"ID": 123,
				"Status": "Active",
				"Lat": 35.51,
				"Lon": -120.51,
				"SensorNodes": [{
						"ID": 1,
						"Status": "Active",
						"Lat": 35.52,
						"Lon": -120.51
					}
				]
			}, {
				"ID": 456,
				"Status": "Active",
				"Lat": 35.42,
				"Lon": -120.42,
				"SensorNodes": [{
						"ID": 4,
						"Status": "Active",
						"Lat": 35.42,
						"Lon": -120.4
					}
				]
			}]
		}
	elif farmname=="AndersonLakeFarm":
		value = {
			"ClusterNodes": [{
				"ID": 123,
				"Status": "Active",
				"Lat": 35.51,
				"Lon": -122.51,
				"SensorNodes": [{
						"ID": 1,
						"Status": "Active",
						"Lat": 35.52,
						"Lon": -120.51
					}
				]
			}, {
				"ID": 456,
				"Status": "Active",
				"Lat": 35.42,
				"Lon": -120.42,
				"SensorNodes": [{
						"ID": 4,
						"Status": "Active",
						"Lat": 35.32,
						"Lon": -121.4
					}
				]
			}]
		}
	return value