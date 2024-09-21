from django.db import models
from django.contrib.auth.models import User
import uuid





class Category(models.Model):
   #id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'categories'


    def __str__(self):
        return self.name
    

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='ecoomerce_pics', blank=True, null=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return self.name

class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='ecoomerce_pics', blank=True, null=True)


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class OrderProduct(models.Model):
    choices = [
        ('PENDING', 'pending'),
        ('DELIVERED', 'deliverd'),
        ('CANCELLED', 'cancelled')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, choices=choices, default='PENDING')


    def __str__(self):
        return self.status
    
    @property
    def total_price(self):
        items = self.items.all()
        total = sum([item.quantity * item.product.price for item in items])
        return total
    

class OrderItem(models.Model):
    order = models.ForeignKey(OrderProduct, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.product.name
    


class Payment(models.Model):
    mode_of_payment = [
        ('BANK TRANSFER', 'bank transfer'),
        ('STRIPE', 'stripe'),
    ]
    order = models.ForeignKey(OrderProduct, on_delete=models.CASCADE)
    mode_of_payment = models.CharField(max_length=100, choices=mode_of_payment, default='BANK TRANSFER')
    payment_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.mode_of_payment,  ': ', self.amount
    


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=100)


    def __str__(self):
        if len(self.street_address) > 25:
            return self.street_address[:25]
        else:
            return self.street_address
        

#Wishlist for future purchase
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

#Cart for immediate purchase 

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Cart: " + str(self.id)
        

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)


class Profile(models.Model):
    name = models.CharField(max_length=200)
    bio = models.TextField()
    picture = models.ImageField(upload_to='ecoomerce_pics', blank=True, null=True)

    def __str__(self):
        return self.name
    

