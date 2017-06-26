from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve
from . import views

urlpatterns = [
	url(r'^$', views.feed, name='feed'),
	url(r'^create$', views.create, name='create'),
	url(r'^project/(?P<project_id>[0-9]+)$', views.project, name='project'),
	url(r'^project/(?P<project_id>[0-9]+)/up$', views.project_up, name='project_up'),
	url(r'^project/(?P<project_id>[0-9]+)/down$', views.project_down, name='project_down'),
]

if settings.DEBUG:
	urlpatterns += [
		url(r'^media/(?P<path>.*)$', serve, {
				'document_root': settings.MEDIA_ROOT,
			}),
	]
