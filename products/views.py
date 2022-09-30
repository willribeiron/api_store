from rest_framework import mixins, viewsets
from products.serializers import ProductSerializer, PurchaseSerializer, StoreSerializer, CustomerSerializer
from .models import Product, Purchase, Store, Customer


class ProductsViewsets(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class StoreViewsets(viewsets.ModelViewSet):
    serializer_class = StoreSerializer
    queryset = Store.objects.all()


class CustomerViewsets(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()


class New_Purchase(mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = PurchaseSerializer
    queryset = Purchase.objects.all()
