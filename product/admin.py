from django.contrib import admin
from .models import SearchProduct
from .models import Product

# Register your models here to be viewed in the admin dashboard
admin.site.register(SearchProduct)
admin.site.register(Product)
