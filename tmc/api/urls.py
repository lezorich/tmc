from django.urls import path

from api import views

urlpatterns = [path("tmc/", views.TMCView.as_view())]
