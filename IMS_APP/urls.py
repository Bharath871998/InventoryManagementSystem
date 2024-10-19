from django.urls import path
from . import views

urlpatterns = [
    # User Authentication Urls
    path('signup', views.signup, name='signup'),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),

    # Below 2 urls are for Product listing and it's detail for Public views
    path('', views.products, name='products'), # This is HOME page
    path('product/<int:pk>/', views.product_detail, name='product_detail'),

    # Below 3 urls are for CRUD operation by Admin only
    path('product/create', views.create_product, name='create_product'),
    path('product/<int:pk>/edit/', views.update_product, name='update_product'),
    path('product/<int:pk>/delete/', views.delete_product, name='delete_product'), 

    # Stock Changes Url
    path('product/<int:pk>/change_stock/', views.change_product_stock, name='change_stock'),  

    # Admin Dashboard Report url
    path('report/', views.report_view, name='report_view'), 
    
]




