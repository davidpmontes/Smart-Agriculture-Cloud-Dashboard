from django.shortcuts import render

def home(request):
	return render(request, 'main/home.html')

def about(request):
	return render(request, 'main/about.html')

def map(request):
	return render(request, 'main/map.html')

def graphs(request):
	return render(request, 'main/graphs.html')
