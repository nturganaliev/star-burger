import rest_framework

from django.urls import path, include

from .views import product_list_api, banners_list_api, register_order


app_name = "foodcartapp"

urlpatterns = [
    path('api_auth/', include('rest_framework.urls')),
    path('products/', product_list_api),
    path('banners/', banners_list_api),
    path('order/', register_order),
]
