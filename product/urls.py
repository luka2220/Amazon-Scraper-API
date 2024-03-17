from django.urls import path

from product import views

urlpatterns = [
    path('search/<str:product_name>', views.search_product),
    path('<str:product_id>', views.product_data)
]
