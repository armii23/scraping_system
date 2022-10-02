from django.contrib import admin
from django.urls import path
from webScraping.views import *

urlpatterns = [
    path('', InternshipView.as_view(), name='internship-list'),
]
