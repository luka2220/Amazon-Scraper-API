# Generated by Django 5.0.3 on 2024-03-19 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0005_alter_product_price"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="sale_data",
            field=models.JSONField(default=dict),
        ),
    ]