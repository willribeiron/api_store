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
        fields = ["product", "store", "customer", "total_price"]


    def stock_quantity_positive(self, lista_de_produtos):
        """
        lista_de_produtos =[{'product': <Product: Product object (d073a038-0b5e-4577-b460-22f99149a410)>, 'quantity': 2}, 
        {'product': <Product: Product object (10ec271d-c661-4f3d-b790-2cad2233a286)>, 'quantity': 3}]
        """
        for product in lista_de_produtos:
            if  product["quantity"] >= product["product"].stock_quantity:
                raise serializers.ValidationError(f"Insufficient stock! Current stock for product {product['product'].description} is {product['product'].stock_quantity}.")


    def customer_money_positive(self, customer, total_price):
        if total_price > customer.money:
            raise serializers.ValidationError(f"Total purchase value {total_price} is higher than money available! "
                                              f"Current money is {customer.money}")

    def money_transaction(self, total_price, customer, store):
        customer.money -= total_price
        store.money += total_price
        customer.save()
        store.save()

    def _get_products(self, products):
        product_list= []
        for product in products:
            purchase_product = Product.objects.get(id=product["id"])
            new_product = {"product": purchase_product, "quantity": product["quantity"]}
            product_list.append(new_product)
        return product_list
    
    def _stock_control(self, lista_de_produtos):
        for product in lista_de_produtos:
            product["product"].stock_quantity -= product["quantity"]
            product["product"].save()
    def _get_total_price(self, lista_de_produtos):
        valor = []
        for product in lista_de_produtos:
            valor_total_produtos = product["product"].price * product["quantity"]
            valor.append(valor_total_produtos)
        return sum(valor)
        
    def create(self, validated_data):
        products = self._get_products(products=validated_data["product"])
        self.stock_quantity_positive(lista_de_produtos=products)
        total_price = self._get_total_price(lista_de_produtos=products)
        self._stock_control(lista_de_produtos=products)
        self.customer_money_positive(customer=validated_data["customer"], total_price=total_price)
        self.money_transaction(total_price=total_price,customer=validated_data["customer"] , store=validated_data["store"])
        purchase = Purchase.objects.create(product=validated_data["product"], store=validated_data["store"], customer=validated_data["customer"], total_price=total_price)
        return purchase

    def get_total_price(self, instance):
        return instance.total_price

