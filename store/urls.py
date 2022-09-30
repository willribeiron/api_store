from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from products.views import New_Purchase, ProductsViewsets, StoreViewsets, CustomerViewsets

router = DefaultRouter()
router.register(r"product", ProductsViewsets, basename="product")
router.register(r"store", StoreViewsets, basename="store")
router.register(r"customer", CustomerViewsets, basename="customer")
router.register(r"purchase", New_Purchase, basename="purchase")
urlpatterns = [
    path("admin/", admin.site.urls),
]

urlpatterns += router.urls
