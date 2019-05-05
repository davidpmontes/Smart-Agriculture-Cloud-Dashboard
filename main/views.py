from django.shortcuts import render, redirect
from django.contrib import messages
from requests.exceptions import ConnectionError
from . forms import NetworkCreationForm, NetworkDeletionForm, FarmEditForm, SensorNodeForm, ClusterNodeForm, SensorForm, SensorDeletionForm
import requests
import urllib.parse
from django.contrib.auth.models import User


url = "http://ec2-3-81-30-51.compute-1.amazonaws.com:8080/"


def editFarm(request, farmid=''):
	if request.method == 'POST':
		form = FarmEditForm(request.POST)
		if form.is_valid():
			if (farmid=='newfarm'):
				networkID = request.POST['networkID']
				name = request.POST['name']
				farmType = request.POST['farmType']
				userID = request.POST['userID']
				lat = request.POST['lat']
				lon = request.POST['lon']


				data = {
					'networkID': networkID,
					'name': name,
					'type': farmType,
					'userID': userID,
					'lat': float(lat),
					'lon': float(lon)
				}

				try:
					requests.post(url = url + "addFarm", data = data)
					messages.success(request, f'Farm created!')
				except:
					messages.error(request, f'Uh oh, there was a problem creating your farm.  Please try again later.')

			else:
				# try:
				# 	requests.post(url = url + "createFarm", data = data)
				# 	messages.success(request, f'Your new network has been created!')
				# except:
				# 	messages.success(request, f'Your new network has been created!')
				# 	messages.error(request, f'Uh oh, there was a problem creating your network.  Please try again later.')

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
			farmID = int(farmid)
			lat = request.POST['lat']
			lon = request.POST['lon']

			data = {
				'farmID': farmID,
				'lat': float(lat),
				'lon': float(lon)
			}
			try:
				requests.post(url = url + "addClusterNode", data = data)
				messages.success(request, f'New Cluster Node created!')
			except:
				messages.error(request, f'Uh oh, there was a problem creating your cluster node.  Please try again later.')
			return redirect('main-adminmapdetails', farmname=farmname, farmid=farmid)

	else:
		form = ClusterNodeForm()

	return render(request, 'main/addClusterNode.html', {'form': form, 'farmid': farmid})

def allfarmersmaps(request, username=''):
	userID = request.user.email
	data = {
		'userID': userID
	}

	try:
		displayInfo = requests.get(url = url + "getFarmbyUserID", params = data).json()
	except:
		print("allfarmersmaps error")

	return render(request, 'main/allfarmersmaps.html', {"displayInfo": displayInfo})

def farmermapdetails(request, farmname='', farmid=''):
	data = {
		'farmID': farmid
	}

	try:
		getFarmbyID = requests.get(url = url + "getFarmbyID", params = data).json()
		getNodesinFarm = requests.get(url = url + "getNodesinFarm", params = data).json()
	except:
		print("allfarmersmaps error")

	return render(request, 'main/farmermapdetails.html', {"farmname": farmname,
														  "farmid": farmid,
														  "getFarmbyID": getFarmbyID,
														  "getNodesinFarm": getNodesinFarm
														  })

def adminmapdetails(request, farmname='', farmid=''):
	data = {
		'farmID': farmid
	}
	try:
		getFarmbyID = requests.get(url = url + "getFarmbyID", params = data).json()
		getNodesinFarm = requests.get(url = url + "getNodesinFarm", params = data).json()
	except:
		print("adminmapdetails error")

	return render(request, 'main/adminmapdetails.html', {"farmname": farmname,
														 "farmid": farmid,
														 "getFarmbyID": getFarmbyID,
														 "getNodesinFarm": getNodesinFarm })

def allusers(request):
	return render(request, 'main/allUsers.html')


def allfarms(request, networkname=''):
	data = {
		'networkID': networkname
	}

	try:
		getNetworkbyID = requests.get(url = url + "getNetworkbyID", params = data).json()
		getFarmsInNetwork = requests.get(url = url + "getFarmsInNetwork", params = data).json()
	except:
		print("getFarmsInNetwork error")
	print(getFarmsInNetwork)

	return render(request, 'main/allfarms.html', {"networkname": networkname,
												  "getNetworkbyID": getNetworkbyID,
												  "getFarmsInNetwork": getFarmsInNetwork})

def allnetworks(request):
	try:
		results = requests.get(urllib.parse.urljoin(url, "getAllNetwork")).json()
	except:
		results = "-1"
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
			networkID = request.POST['networkName']
			lat = request.POST['lat']
			lon = request.POST['lon']
			data = {
				'networkID': networkID,
				'lat': float(lat),
				'lon': float(lon)
			}

			#call api
			existingNetworkNames = ['farm1', 'farm2']

			if form.cleaned_data.get('networkName') in existingNetworkNames:
				messages.error(request, f'That network name already exists')
			else:
				try:
					requests.post(url = url + "createNetwork", data = data)
					messages.success(request, f'Your new network has been created!')
				except:
					messages.error(request, f'Uh oh, there was a problem creating your network.  Please try again later.')
				return redirect('main-home')
	else:
		form = NetworkCreationForm()

	return render(request, 'main/createNetwork.html', {'form': form})



def home(request, id=''):
	try:
		getFarmTotalwithType = requests.get(urllib.parse.urljoin(url, "getFarmTotalwithType"), timeout=3).json()
		getAllNetwork = requests.get(urllib.parse.urljoin(url, "getAllNetwork"), timeout=3).json()
		getAllNetworkHeath = requests.get(urllib.parse.urljoin(url, "getAllNetworkHeath"), timeout=3).json()
		getFarmsTotal = requests.get(urllib.parse.urljoin(url, "getFarmTotal"), timeout=3).json()
		getUsersTotal = len(User.objects.all())
		getSensorsTotal = 15
	except: 
		getFarmTotalwithType = "error"
		getAllNetwork = "error"
		getAllNetworkHeath = "error"
		getFarmsTotal = "error"
		getUsersTotal = "error"
		getSensorsTotal = "error"

	return render(request, 'main/home.html', {"getFarmTotalwithType": getFarmTotalwithType,
											  "getAllNetwork": getAllNetwork,
											  "getAllNetworkHeath": getAllNetworkHeath,
											  "getFarmsTotal": getFarmsTotal,
											  "getUsersTotal": getUsersTotal,
											  "getSensorsTotal": getSensorsTotal
											  })

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