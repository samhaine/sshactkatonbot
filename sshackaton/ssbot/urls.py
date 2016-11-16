from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^ssbotendpoint/(.*)', views.get_json),