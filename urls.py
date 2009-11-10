from django.conf.urls.defaults import *
from django.conf import settings
from os import path as os_path

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^sequias/', include('sequias.foo.urls')),
#    (r'^', include('sequias.urls')),
    (r'^$', 'sequias.views.index'),
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)

if (settings.DEBUG == True):
    urlpatterns += patterns('',
                            (r'^media/(.*)$', 'django.views.static.serve', {'document_root': os_path.join(settings.MEDIA_ROOT)}),
                        )

