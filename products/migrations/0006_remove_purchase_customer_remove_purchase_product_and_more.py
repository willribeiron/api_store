# Generated by Django 4.1.1 on 2022-09-27 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0005_alter_product_price"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="purchase",
            name="customer",
        ),
        migrations.RemoveField(
            model_name="purchase",
            name="product",
        ),
        migrations.RemoveField(
            model_name="purchase",
            name="store",
        ),
        migrations.AddField(
            model_name="purchase",
            name="purchase",
            field=models.JSONField(default=None),
            preserve_default=False,
        ),
    ]
