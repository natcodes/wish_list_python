from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^registration$', views.registration), 
    url(r'^login$', views.login), 
    url(r'^home$', views.home), #success or dashboard page
    url(r'^logout$', views.logout),
    url(r'^create$', views.create),
    url(r'^create_page$', views.create_page),
    url(r'^delete/(?P<id>\w+)$', views.delete),
    url(r'^addwish/(?P<id>\w+)$', views.addwish), 
    url(r'^removewish/(?P<id>\w+)$', views.removewish),
    url(r'^wish_item/(?P<id>\w+)$', views.wish_item)
]

