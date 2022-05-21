from django.urls import path
from stock_chase.views import home, add_product, list_products, toggle_product, \
    delete_product, edit_product, trade_now, edit_product_group, increase_stock, reduce_stock

urlpatterns = [
    path('', home, name="home"),
    path('list-products/', list_products, name="list_products"),
    path('delete-product/<str:pk>/', delete_product, name="delete_product"),
    path('add-product/', add_product, name="add_product"),
    path('edit-product/<str:pk>/', edit_product, name="edit_product"),
    path('edit-product-group/<str:pk>/', edit_product_group, name="edit_product_group"),
    path('toggle-product-status/<str:pk>/', toggle_product, name="toggle_product_status"),
    path('trade-now/', trade_now, name="trade_now"),
    path('increase-stock/<str:pk>/', increase_stock, name="increase_stock"),
    path('reduce-stock/<str:pk>/', reduce_stock, name="reduce_stock"),

]
