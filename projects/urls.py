from . import views
from django.urls import path

urlpatterns = [
    path('', views.ProjectList.as_view(), name='projects'),
]