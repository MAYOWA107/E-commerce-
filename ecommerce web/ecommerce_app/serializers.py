from rest_framework import serializers
from .models import Product, Category, Review, Cart, CartItem, ProductImages, Profile, OrderProduct, OrderItem


from django.db import transaction


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description']


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImages
        fields = ['id', 'product', 'image']


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True)
    uploaded_images = serializers.ListField(
        child= serializers.ImageField(max_length=1000000, allow_empty_file = False, use_url = False),
        write_only=True
    )
    class Meta:
        model = Product
        fields = ['id', 'category', 'name', 'slug', 'price', 'description', 'images', 'uploaded_images']

    category = serializers.StringRelatedField()
   # category = CategorySerializer()


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['description', 'date_created']

    def create(self, validated_data):
        product_id = self.context["product_id"]
        name = self.context["name"]
        return Review.objects.create(product_id=product_id, name=name, **validated_data)


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']




class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(many=False)
    sub_total = serializers.SerializerMethodField(method_name="sub_total_price")
    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'quantity', 'sub_total']

    def sub_total_price(self, cartitem:CartItem):
        total = cartitem.quantity * cartitem.product.price
        return total


class AddCartItemSerializer(serializers.ModelSerializer):
    
    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product = self.validated_data['product']
        quantity = self.validated_data['quantity']

        try:
            cartitem = CartItem.objects.get(product=product, cart_id=cart_id)    
            cartitem.quantity += quantity
            cartitem.save()
            self.instance = cartitem

        except:
            cartitem = CartItem.objects.create(product=product, cart_id=cart_id, quantity=quantity)
            self.instance= cartitem

        return self.instance
    class Meta:
        model = CartItem
        fields = ['product', 'quantity']






class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only = True)
    total = serializers.SerializerMethodField(method_name='total_price')
    class Meta:
        model = Cart
        fields = ['id', 'items', 'total']

    def total_price(self, cart:Cart):
        items = cart.items.all()
        total = sum([item.quantity * item.product.price for item in items])
        return total
        
class UpdateCartItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CartItem
        fields = ['quantity']



class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['id', 'name', 'bio', 'picture']


class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(read_only=True)
    class Meta:
        model = OrderItem
        fields = ['order', 'product', 'quantity']


class OrderProductSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = OrderProduct
        fields = ['id', 'status', 'order_date', 'items']

    
class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.IntegerField()
    

    def save(self, **kwargs):

        with transaction.atomic():
            cart_id = self.validated_data['cart_id']
            user_id = self.context['user_id']
            #user has to login for them to create order
            order = OrderProduct.objects.create(user_id=user_id)

            #create order base on cart_id
            cartitems = CartItem.objects.filter(cart_id=cart_id)
            
            orderitems = [
                OrderItem(order=order, product=item.product, quantity=item.quantity)
                for item in cartitems
            ]
            OrderItem.objects.bulk_create(orderitems)
            #delete the cart once order has been placed.

            Cart.objects.filter(id=cart_id).delete()