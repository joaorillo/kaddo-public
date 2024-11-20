from django.urls import path

from . import views

urlpatterns = [
    path('aisles/', views.aisles, name="aisles_list"),
    path('aisles/<str:slug>', views.aisles, name="aisle_detail"),
    path('bulk_update/', views.bulk_update, name="bulk_update"),
    path('categories/', views.categories, name="categories_list"),
    path('categories/<str:slug>', views.categories, name="category_detail"),
    path('generate_api_key/', views.generate_api_key, name="generate_api_key"),
    path('search/', views.search, name="search"),
]
