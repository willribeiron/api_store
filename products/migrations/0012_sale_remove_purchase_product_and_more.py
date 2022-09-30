# Generated by Django 4.1.1 on 2022-09-29 13:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0011_remove_purchase_product_purchase_product"),
    ]

    operations = [
        migrations.CreateModel(
            name="Sale",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
        ),
        migrations.RemoveField(
            model_name="purchase",
            name="product",
        ),
        migrations.AddConstraint(
            model_name="purchase",
            constraint=models.UniqueConstraint(
                fields=("product", "sale"), name="per_sale_product"
            ),
        ),
        migrations.AddField(
            model_name="sale",
            name="product",
            field=models.ManyToManyField(
                through="products.Purchase", to="products.product"
            ),
        ),
        migrations.AddField(
            model_name="purchase",
            name="sale",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="products.sale",
            ),
        ),
        migrations.AddField(
            model_name="purchase",
            name="product",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="products.product",
            ),
        ),
    ]
