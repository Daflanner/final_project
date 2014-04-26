from django.conf.urls import url, patterns 
from counter import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^register/$', views.register, name='register'),
	url(r'^login/$', views.user_login, name='login'),
	url(r'^logout/$', views.user_logout, name='logout'),
	url(r'^Day_Record/$', views.Day_Record,  name='Day_Record'),
	#url(r'^MealEntry/$', views.MealEntry,  name='MealEntry')
	url(r'^(?P<year>[0-9]{4})-(?P<month>[0-9]{2})-(?P<day>[0-9]{2})/$', views.MealEntry, name = 'MealEntry'  ), 
	url(r'^Component/$', views.Component, name = 'Component'  ), 
	#url(r'^restricted/', views.restricted, name='restricted'),         

)