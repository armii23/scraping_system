from django.contrib import admin
from django.urls import path
from webScraping.views import *
from . import views

urlpatterns = [
    path('', InternshipView.as_view(), name='internship-list'),
    path('category/<slug:cat_slug>/', InternshipCategoryView.as_view(), name='category'),
    path('fav/<int:id>/', views.favourite_add, name='favourite_add'),
    path('favourite/', views.favourite_list, name='favourite_list'),
]