from django.urls import path, include
from .views import CategoryViewset, ProductViewset, ReviewViewset, CartViewset, CartItemViewsert, ProfileViewset, OrderViewset, OrderItemViewset
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers


router = routers.DefaultRouter()
router.register('category', CategoryViewset)
router.register('products', ProductViewset)
router.register('carts', CartViewset)
router.register('profiles', ProfileViewset)
router.register('orders', OrderViewset, basename='orders')


product_router = routers.NestedDefaultRouter(router, "products", lookup="product")
product_router.register("reviews", ReviewViewset, basename="product-review")

cart_router = routers.NestedDefaultRouter(router, 'carts', lookup='carts')
cart_router.register('items', CartItemViewsert, basename='items')




urlpatterns = [
    path('', include(router.urls)), 
    path('', include(product_router.urls)),
    path('', include(cart_router.urls)),

    path('', include('rest_framework.urls')),
   #path('', CategoryListView.as_view(), name='categories'),
   #path('category/<int:pk>', CategoryDetailView.as_view(), name='category'),
    #path('products', ProductListView.as_view(), name='products'),
    #path('product/<int:pk>/', ProductDetailView.as_view(), name='product'),
]