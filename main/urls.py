from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name='main-home'),
	path('<int:id>', views.home, name='main-home'),
	path('allnetworks/', views.allnetworks, name='main-allnetworks'),

	path('allfarms/', views.allfarms, name='main-allfarms'),
	path('allfarms/<str:networkname>', views.allfarms, name='main-allfarms'),

	path('adminmapdetails/', views.adminmapdetails, name='main-adminmapdetails'),
	path('adminmapdetails/<str:farmname>', views.adminmapdetails, name='main-adminmapdetails')
]