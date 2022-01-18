from django.urls import path, include
from . import views

urlpatterns = [

    path("upload-file/", views.HomeView, name='upload-file'),

]
