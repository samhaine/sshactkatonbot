from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^botendpoint', views.botendpoint, name='botendpoint'),
    #url(r'^gettoken', views.getJWTtoken, name='getJWTtoken'),
    ]