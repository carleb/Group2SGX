
from django.urls import path

from . import views

urlpatterns = [


    # Store main page

    path('', views.store, name='store'),


    # Individual product

    path('product/<slug:product_slug>/', views.product_info, name='product-info'),

    path('store/upload_product' ,views.upload_product, name='upload-product'),

    path('sales/sales_report', views.get_top_items, name='sales-report')


]
