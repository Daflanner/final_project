from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'calMachine.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^counter/', include('counter.urls')),
    url(r'^admin/', include(admin.site.urls)),
   
    )
#if settings.DEBUG:
      #  urlpatterns += patterns(
       #         'django.views.static',
        #        (r'media/(?P<path>.*)',
         #       'serve',
          #      {'document_root': settings.MEDIA_ROOT}), )