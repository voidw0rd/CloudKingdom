from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	url(r"^$", "CloudManager.views.index", name = "index"),
    # url(r'^$', 'CloudKingdom.views.home', name='home'),
    # url(r'^CloudKingdom/', include('CloudKingdom.foo.urls')),

    

)
