from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name='main-home'),
	path('about/', views.about, name='main-about'),
	path('map/', views.map, name='main-map'),
	path('graphs/', views.graphs, name='main-graphs'),
]