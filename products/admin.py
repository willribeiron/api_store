from django.contrib import admin

# Register your models here.
from products.models import Purchase, Product, Store, Customer

admin.site.register(Product)
admin.site.register(Store)
admin.site.register(Customer)


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    readonly_fields = ["id", "created_at", "updated_at"]
