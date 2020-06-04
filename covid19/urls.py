from . import views
from django.urls import path


urlpatterns = [
    path('', views.CovidDetail.as_view(), name='covid'),
]