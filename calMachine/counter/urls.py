from django.conf.urls import url, patterns 
from counter import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^register/$', views.register, name='register'),
	url(r'^login/$', views.user_login, name='login'),
	url(r'^Day_Record/$', views.Day_Record,  name='Day_Record'),
	url(r'^MealEntry/$', views.MealEntry,  name='MealEntry')


	)