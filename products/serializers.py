from rest_framework import serializers
from products.models import Product, Purchase, Store, Customer

class ProductSerializer(serializers.ModelSerializer):
    available = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["description", "price", "stock_quantity", "available"]

    def validate(self, data):
        product = Product.objects.filter(description=data["description"]).first()
        if product:
            raise serializers.ValidationError("Product already exists")
        return data

    def get_available(self, instance):
        if instance.stock_quantity > 0:
            return True
        return False


class StoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Store
        fields = ["name", "money"]

    def validate(self, data):
        store = Store.objects.filter(name=data["name"]).first()
        if store:
            raise serializers.ValidationError("Store already exists")
        return data


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ["name", "money"]

    def validate(self, data):
        customer = Customer.objects.filter(name=data["name"]).first()
        if customer:
            raise serializers.ValidationError("Customer already exists")
        return data


class PurchaseSerializer(serializers.ModelSerializer):
    total_price = serializers.DecimalField(decimal_places=2, max_digits=9, read_only=True)

    class Meta:
        model = Purchase
        fields = ["product", "store", "customer", "total_price", "quantity"]


    def stock_quantity_positive(self, stock_quantity, quantity):
        if quantity > stock_quantity:
            raise serializers.ValidationError(f"Insufficient stock! Current stock is {stock_quantity}.")


    def customer_money_positive(self, customer, total_price):
        if total_price > customer.money:
            raise serializers.ValidationError(f"Total purchase value {total_price} is higher than money available! "
                                              f"Current money is {customer.money}")

    def money_transaction(self, total_price, customer, store):
        customer.money -= total_price
        store.money += total_price
        customer.save()
        store.save()

    def stock_control(self, product, quantity):
        product.stock_quantity -= quantity
        product.save()

    def validate(self, data):
        stock_quantity = data["product"].stock_quantity
        quantity = data["quantity"]
        price = data["product"].price
        total_price = price * quantity
        customer = data["customer"]
        self.stock_quantity_positive(stock_quantity, quantity)
        self.customer_money_positive(customer, total_price)
        return data

    def create(self, validated_data):
        product = validated_data["product"]
        store = validated_data["store"]
        customer = validated_data["customer"]
        quantity = validated_data["quantity"]
        price = validated_data["product"].price
        total_price = price * quantity
        purchase = Purchase.objects.create(product=product, store=store, customer=customer, quantity=quantity,
                                           total_price=total_price)
        self.stock_control(product, quantity)
        self.money_transaction(total_price, customer, store)
        return purchase

    def get_total_price(self, instance):
        return instance.total_price

