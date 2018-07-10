from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^dashboard$', views.dashboard),
    url(r'^addFriend/(?P<id>\d+)$', views.addFriend),
    url(r'^user/(?P<id>\d+)$', views.showUser), #?P<id>\d+ is required to pass an id variable into the route
    url(r'^remove/(?P<id>\d+)$', views.removeFriend)
]