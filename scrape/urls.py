from django.urls import path
from . import views

urlpatterns=[path("aajtak/",views.aajtak),path("ndtv/",views.ndtv),path("post/",views.post)]
