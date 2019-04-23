from django.shortcuts import render, redirect
from django.contrib import messages
from requests.exceptions import ConnectionError
from . forms import NetworkCreationForm, NetworkDeletionForm
import requests

def adminmapdetails(request, farmname=''):
	displayInfo = GetFarmNodes(farmname)
	return render(request, 'main/adminmapdetails.html', {"farmname": farmname, "displayInfo": displayInfo})

def allfarms(request, networkname=''):
	return render(request, 'main/allfarms.html', {"networkname": networkname})

def allnetworks(request):
	return render(request, 'main/allnetworks.html')


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
	#sijiaurl = "http://ec2-184-73-33-184.compute-1.amazonaws.com:8080/"

	#response = requests.get(sijiaurl)
	#result = response.json()

	return render(request, 'main/home.html') #, {"result": result})

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