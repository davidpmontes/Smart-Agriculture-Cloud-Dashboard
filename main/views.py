from django.shortcuts import render, redirect
from django.contrib import messages
from requests.exceptions import ConnectionError
from . forms import NetworkCreationForm, NetworkDeletionForm, FarmEditForm, SensorNodeForm, ClusterNodeForm, SensorForm, SensorDeletionForm, SensorNodeDeletionForm, ClusterNodeDeletionForm
import requests
import urllib.parse
from django.contrib.auth.models import User



url = "http://ec2-3-81-30-51.compute-1.amazonaws.com:8080/"


def editFarm(request, farmid=''):
	getAllNetworkID = []
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

	return render(request, 'main/editFarm.html', {'form': form,
												  'farmid': farmid})



def addSensor(request, sensornodeid=''):
	if request.method == 'POST':
		form = SensorForm(request.POST)
		if form.is_valid():
			sensornodeid = int(sensornodeid)
			sensorID = request.POST['sensorID']
			sensorType = request.POST['sensorType']
			status = request.POST['status']

			data = {
				'sensornodeid': sensornodeid,
				'sensorID': sensorID,
				'type': sensorType,
				'status': status
			}

			try:
				requests.post(url=url + "addSensor", data=data)
				messages.success(request, f'New Sensor created!')
			except:
				messages.error(
					request, f'Uh oh, there was a problem creating your sensor.  Please try again later.')
			return redirect('main-home')
	else:
		form = SensorForm()

	return render(request, 'main/addSensor.html', {'form': form, 'sensornodeid': sensornodeid, 'name': 'david'})


def addSensorNode2(request, farmname='', farmid='', clusternodeid=''):
	if request.method == 'POST':
		form = SensorNodeForm(request.POST)
		if form.is_valid():
			clusternodeid = int(clusternodeid)
			lat = request.POST['lat']
			lon = request.POST['lon']

			data = {
				'clusternodeid': clusternodeid,
				'lat': float(lat),
				'lon': float(lon)
			}

			try:
				requests.post(url=url + "addSensorNode", data=data)
				messages.success(request, f'New Sensor Node created!')
			except:
				messages.error(
					request, f'Uh oh, there was a problem creating your sensor node.  Please try again later.')

			return redirect('main-adminmapdetails', farmname, farmid)
	else:
		form = SensorNodeForm()

	return render(request, 'main/addSensorNode.html', {'form': form, 'clusternodeid': clusternodeid})

def addSensorNode(request, farmname='', farmid=''):
	if request.method == 'POST':
		form = SensorNodeForm(request.POST)
		if form.is_valid():
			

			return redirect('main-adminmapdetails', farmname=farmname, farmid=farmid)
	else:
		form = SensorNodeForm()

	return render(request, 'main/addSensorNode.html', {'form': form, 'farmid': farmid})

def addClusterNode(request, farmname='', farmid=''):
	if request.method == 'POST':
		form = ClusterNodeForm(request.POST)
		if form.is_valid():
			farmid = int(farmid)
			lat = request.POST['lat']
			lon = request.POST['lon']

			data = {
				'farmid': farmid,
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
	userID = request.user.username
	data = {
		'userID': userID
	}

	try:
		getFarmbyUserID = requests.get(url = url + "getFarmbyUserID", params = data).json()
	except:
		print("allfarmersmaps error")

	return render(request, 'main/allfarmersmaps.html', {"getFarmbyUserID": getFarmbyUserID})

def farmermapdetails(request, farmname='', farmid=''):
	data = {
		'farmID': farmid
	}
	getSensorsinClusterDict = {}
	try:
		getFarmbyID = requests.get(url = url + "getFarmbyID", params = data).json()
		getNodesinFarm = requests.get(url = url + "getNodesinFarm", params = data).json()
		for cluster in getNodesinFarm:
			data2 = {
				'clusternodeid': cluster['clusternodeid']
			}
			getSensorsinCluster = requests.get(url=url + "getSensorsinCluster", params=data2).json()
			getSensorsinClusterDict[cluster['clusternodeid']] = getSensorsinCluster
	except:
		print("allfarmersmaps error")

	return render(request, 'main/farmermapdetails.html', {"farmname": farmname,
														  "farmid": farmid,
														  "getFarmbyID": getFarmbyID,
														  "getNodesinFarm": getNodesinFarm,
                                                       	  "getSensorsinClusterDict": getSensorsinClusterDict
														  })

def adminmapdetails(request, farmname='', farmid=''):
	data = {
		'farmID': farmid
	}
	getSensorsinClusterDict = {}
	try:
		getFarmbyID = requests.get(url = url + "getFarmbyID", params = data).json()
		getNodesinFarm = requests.get(url = url + "getNodesinFarm", params = data).json()
		for cluster in getNodesinFarm:
			data2 = {
				'clusternodeid': cluster['clusternodeid']
			}
			getSensorsinCluster = requests.get(url=url + "getSensorsinCluster", params=data2).json()
			getSensorsinClusterDict[cluster['clusternodeid']] = getSensorsinCluster

	except:
		print("adminmapdetails error")

	return render(request, 'main/adminmapdetails.html', {"farmname": farmname,
														 "farmid": farmid,
														 "getFarmbyID": getFarmbyID,
														 "getNodesinFarm": getNodesinFarm,
                                                      	 "getSensorsinClusterDict": getSensorsinClusterDict})

def allusers(request):
	allusers = User.objects.all()
	farmDictionary = {}


	for user in allusers:
		data = { 'userID': user }
		try:
			farmList = requests.get(url = url + "getFarmbyUserID", params = data).json()
			farmDictionary[str(user)] = farmList
			#alluserfarms.append(farmDictionary)
		except:
			print("all users error")
	
	return render(request, 'main/allUsers.html', {'allusers': allusers,
												  'farmDictionary': farmDictionary})


def allfarms(request, networkid=''):
	data = {
		'networkID': networkid
	}

	try:
		getNetworkbyID = requests.get(url = url + "getNetworkbyID", params = data).json()
		getFarmsInNetwork = requests.get(url = url + "getFarmsInNetwork", params = data).json()
		print(getFarmsInNetwork)
	except:
		print("getFarmsInNetwork error")

	return render(request, 'main/allfarms.html', {"networkid": networkid,
												  "getNetworkbyID": getNetworkbyID,
												  "getFarmsInNetwork": getFarmsInNetwork})

def allnetworks(request):
	try:
		results = requests.get(urllib.parse.urljoin(url, "getAllNetwork")).json()
	except:
		results = "-1"
	return render(request, 'main/allnetworks.html', {"results": results})


def deleteClusterNode(request, clusternodeid=''):
	if request.method == 'POST':
		form = ClusterNodeDeletionForm(request.POST)
		if form.is_valid():
			data = {
				'clusternodeID': clusternodeid,
			}

			try:
				requests.post(url=url + "deleteClusterNode", data=data)
				messages.success(request, f'Cluster node deleted')
			except:
				messages.error(
					request, f'Uh oh, there was a problem deleting your cluster node.  Please try again later.')

			return redirect('main-home')
	else:
		form = SensorDeletionForm()

	return render(request, 'main/deleteClusterNode.html', {'form': form, 'clusternodeid': clusternodeid})


def deleteSensorNode(request, sensornodeid=''):
	if request.method == 'POST':
		form = SensorNodeDeletionForm(request.POST)
		if form.is_valid():
			data = {
				'sensornodeid': sensornodeid,
			}

			try:
				requests.post(url=url + "deleteSensorNode", data=data)
				messages.success(request, f'Sensor node deleted')
			except:
				messages.error(
					request, f'Uh oh, there was a problem deleting your sensor node.  Please try again later.')

			return redirect('main-home')
	else:
		form = SensorDeletionForm()

	return render(request, 'main/deleteSensorNode.html', {'form': form, 'sensornodeid': sensornodeid})


def deleteSensor(request, sensorid=''):
	if request.method == 'POST':
		form = SensorDeletionForm(request.POST)
		if form.is_valid():
			data = {
				'sensorID': sensorid,
			}

			try:
				requests.post(url=url + "deleteSensor", data=data)
				messages.success(request, f'Sensor deleted')
			except:
				messages.error(
					request, f'Uh oh, there was a problem deleting your sensor.  Please try again later.')

			return redirect('main-home')
	else:
		form = SensorDeletionForm()

	return render(request, 'main/deleteSensor.html', {'form': form, 'sensorid': sensorid})


def deleteFarm(request, farmid=''):
	if request.method == 'POST':
		form = SensorDeletionForm(request.POST)
		if form.is_valid():
			data = {
				'farmID': farmid,
			}

			try:
				requests.post(url=url + "deleteFarm", data=data)
				messages.success(request, f'Farm deleted')
			except:
				messages.error(
					request, f'Uh oh, there was a problem deleting your farm.  Please try again later.')

			return redirect('main-home')
	else:
		form = SensorDeletionForm()

	return render(request, 'main/deleteFarm.html', {'form': form, 'farmID': farmid})


def deleteNetwork(request, networkid=''):
	if request.method == 'POST':
		form = NetworkDeletionForm(request.POST)
		if form.is_valid():
			data = {
				'networkID': networkid,
			}

			try:
				response = requests.post(url=url + "deleteNetworkbyID", data=data)
				if response.text.status == "200":
					messages.success(request, f'Network created!')
				else:
					messages.warning(request, response.text)
			except:
				messages.warning(request, response.text)

			return redirect('main-home')
	else:
		form = NetworkDeletionForm()

	return render(request, 'main/deleteNetwork.html', {'form': form, 'networkID': networkid})


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
	data = {
		'userID': request.user.username,
	}

	try:
		getFarmTotalwithType = requests.get(urllib.parse.urljoin(url, "getFarmTotalwithType"), timeout=3).json()
		getSensorTotalwithType = requests.get(urllib.parse.urljoin(url, "getSensorTotalwithType"), timeout=3).json()
		getAllNetwork = requests.get(urllib.parse.urljoin(url, "getAllNetwork"), timeout=3).json()
		getAllNetworkHeath = requests.get(urllib.parse.urljoin(url, "getAllNetworkHeath"), timeout=3).json()
		getFarmsTotal = requests.get(urllib.parse.urljoin(url, "getFarmTotal"), timeout=3).json()
		getUsersTotal = len(User.objects.all())
		getSensorsTotal = requests.get(urllib.parse.urljoin(url, "getSensorTotal"), timeout=3).json()
		getAllFarmHeathbyUser = requests.get(url=url + "getAllFarmHeathbyUser", params=data).json()
		getSensorHealth = requests.get(url=url + "getSensorHealth").json()


	except: 
		getFarmTotalwithType = "error"
		getSensorTotalwithType = "error"
		getAllNetwork = "error"
		getAllNetworkHeath = "error"
		getFarmsTotal = "error"
		getUsersTotal = "error"
		getSensorsTotal = "error"
		getAllFarmHeathbyUser = "error"
		getSensorHealth = "error"

	return render(request, 'main/home.html', {"getFarmTotalwithType": getFarmTotalwithType,
                                           	  "getSensorTotalwithType": getSensorTotalwithType,
											  "getAllNetwork": getAllNetwork,
											  "getAllNetworkHeath": getAllNetworkHeath,
											  "getFarmsTotal": getFarmsTotal,
											  "getUsersTotal": getUsersTotal,
											  "getSensorsTotal": getSensorsTotal,
                                           	  "getAllFarmHeathbyUser": getAllFarmHeathbyUser,
                                           	  "getSensorHealth": getSensorHealth
											  })
