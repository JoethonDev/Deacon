from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="index"),
    path('save', submit_attendance),
    path('names', submit_name),
    path('names/<str:sheet_name>', retrieve_names),
    path('class', submit_class),
]