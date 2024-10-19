from django.urls import path
from . import api_views

urlpatterns = [
    path('products/', api_views.product_list, name='product_list'),
    path('products/<int:pk>/', api_views.product_detail, name='product_detail'),
    path('products/<int:pk>/change_stock/', api_views.change_stock, name='change_stock'),
    # Add more API endpoints as needed
]
