from django.shortcuts import render
from requests.exceptions import ConnectionError
import requests

def home(request, id=''):

	#TODO
	# if id is set, then need to get information about farm
	# GetFarmsByUser(Joe123)
	usersFarms = [1, 2, 3]

	#url = 'http://13.57.209.41:8080/sensors'

	#r = None
	context = None

	try:
		#r = requests.get(url, timeout=0.001)
		context = {
			#'info': r.json(),
			#'data': r.json()[0]['data'][0],
			'id': id,
			'usersFarms': usersFarms,
		}
	except ConnectionError as e:    # This is the correct syntax
#		print(e)
		context = {
			'error': "Hmmm, our server appears to be taking a long time to respond.  Please try again in a few minutes."
		}

	return render(request, 'main/home.html', context)

def about(request):
	return render(request, 'main/about.html')