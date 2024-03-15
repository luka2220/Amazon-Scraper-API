from django.db import models


class SearchProduct(models.Model):
    name = models.TextField
    results = models.JSONField
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content
