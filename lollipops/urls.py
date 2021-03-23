from django.contrib import admin
from django.urls import path, include

from lollipops.views import *

app_name = 'courier'
urlpatterns = [
    path('courier/create', CourierCreateView.as_view()),
    path('all/', CourierListView.as_view()),
    path('courier/detail/<int:pk>/', CourierDetailView.as_view())
]