from django.conf.urls import patterns, include, url
import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	url(r"^$", "CloudManager.views.index", name = "index"),
	url(r"createinstance/$", "CloudManager.views.create", name = "create"),
	url(r"list/$", "CloudManager.views.list", name = "list"),
	url(r"delete/$", "CloudManager.views.delete", name = "delete"),
    # url(r'^$', 'CloudKingdom.views.home', name='home'),
    # url(r'^CloudKingdom/', include('CloudKingdom.foo.urls')),



)


if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_URL,
        }),
)