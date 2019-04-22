from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name='main-home'),
	path('<int:id>', views.home, name='main-home'),
	path('about/', views.about, name='main-about'),
	path('wenpage/', views.wenpage, name='main-wenpage'),
]