from django.contrib import admin

from .models import (Category, Product, OrderProduct, OrderItem, Payment,
                      Wishlist, Cart, CartItem, Review, OrderProduct, OrderItem)



admin.site.register(Category)
admin.site.register(Product) 
admin.site.register(OrderItem) 
admin.site.register(Review)
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(OrderProduct)
