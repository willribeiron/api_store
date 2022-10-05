from django.db import models
from uuid import uuid4
from django.core.serializers.json import DjangoJSONEncoder


class BaseModel(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Product(BaseModel):
    description = models.CharField(max_length=255, blank=False, null=False)
    price = models.DecimalField(decimal_places=2, max_digits=9)
    stock_quantity = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


class Customer(BaseModel):
    name = models.CharField(max_length=255, blank=False, null=False)
    money = models.DecimalField(decimal_places=2, max_digits=9)

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"


class Store(BaseModel):
    name = models.CharField(max_length=255, blank=False, null=False)
    money = models.DecimalField(decimal_places=2, max_digits=9)

    class Meta:
        verbose_name = "Store"
        verbose_name_plural = "Stores"


class Purchase(BaseModel):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, default=None)
    product = models.JSONField(encoder=DjangoJSONEncoder)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default=None)
    total_price = models.DecimalField(decimal_places=2, max_digits=9, default=None)

    class Meta:
        verbose_name = "Purchase"
        verbose_name_plural = "Purchases"
