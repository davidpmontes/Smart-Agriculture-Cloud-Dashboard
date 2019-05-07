from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name='main-home'),
	path('<int:id>', views.home, name='main-home'),

	path('allfarmersmaps/', views.allfarmersmaps, name='main-allfarmersmaps'),
	path('allfarmersmaps/<str:username>', views.allfarmersmaps, name='main-allfarmersmaps'),

	path('allusers/', views.allusers, name='main-allusers'),
	path('allnetworks/', views.allnetworks, name='main-allnetworks'),

	path('allfarms/', views.allfarms, name='main-allfarms'),
	path('allfarms/<str:networkname>', views.allfarms, name='main-allfarms'),

	path('farmermapdetails/<str:farmname>/<str:farmid>', views.farmermapdetails, name='main-farmermapdetails'),

	path('adminmapdetails/', views.adminmapdetails, name='main-adminmapdetails'),
	path('adminmapdetails/<str:farmname>/<str:farmid>', views.adminmapdetails, name='main-adminmapdetails'),

	path('editFarm/<str:farmid>', views.editFarm, name='main-editFarm'),

	path('addClusterNode/<str:farmname>/<str:farmid>', views.addClusterNode, name='main-addClusterNode'),
	path('addSensorNode/<str:farmname>/<str:farmid>', views.addSensorNode, name='main-addSensorNode'),
  	path('addSensorNode2/<str:farmname>/<str:farmid>/<str:clusternodeid>',views.addSensorNode2, name='main-addSensorNode2'),
	
	path('addSensor/<str:sensornodeid>', views.addSensor, name='main-addSensor'),
	path('deleteSensor/<str:sensorid>', views.deleteSensor, name='main-deleteSensor'),
	path('deleteSensorNode/<str:sensornodeid>', views.deleteSensorNode, name='main-deleteSensorNode'),
	path('deleteClusterNode/<str:clusternodeid>', views.deleteClusterNode, name='main-deleteClusterNode'),
]

