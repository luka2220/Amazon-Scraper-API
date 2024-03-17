from django.db import models


class SearchProduct(models.Model):
    name = models.TextField
    results = models.JSONField
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    title = models.TextField(max_length=250)
    price = models.CharField(max_length=20)
    info = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id
