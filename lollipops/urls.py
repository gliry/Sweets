from django.contrib import admin
from django.urls import path, include

from lollipops.views import *

app_name = 'courier'
urlpatterns = [
    path('couriers/', CourierCreateView.as_view()),
    path('couriers/<int:pk>/', CourierDetailView.as_view()),
    path('orders/', OrderCreateView.as_view()),
    path('orders/assign/', OrderAssignView.as_view()),

    path('all_couriers/', CourierListView.as_view()),
    path('all_orders/', OrderListView.as_view()),




]