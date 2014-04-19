from django.conf.urls import url, patterns 
from counter import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^register/$', views.register, name='register'),



	)