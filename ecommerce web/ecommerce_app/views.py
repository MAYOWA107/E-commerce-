#from .models import Product, Category
from . import models

from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import (ProductSerializer, CategorySerializer, ReviewSerializer, ProductImages, ProfileSerializer,
                          CartSerializer,CartItemSerializer, AddCartItemSerializer,
                            UpdateCartItemSerializer, OrderProductSerializer, OrderItemSerializer, CreateOrderSerializer)
from django_filters.rest_framework import DjangoFilterBackend

from .filters import ProductFilter

from rest_framework.parsers import MultiPartParser, FormParser

from django.conf import settings
import requests
import uuid



def initiate_payment(amount, email, order_id):
    url = "https://api.flutterwave.com/v3/payments"
    headers = {
        "Authorization": f"Bearer {settings.FLW_SEC_KEY}"   
    }

    data = {
        "tx_ref": str(uuid.uuid4()),
        "amount": str(amount),
        "currency": "NGN",  
        "redirect_url":  'http://127.0.0.1:8000/orders/confirm_payment/?o_id=' + (order_id),
        "meta":{
            "consumer_id": 23,
            "consumer_mac": "92a3-912ba-1192a",
        },
        "customer": {
            "email": email,
            "phonenumber": "090****3865",
            "name": "Hafeez Mayowa",
        },
        "customizations": {
            "title": "Pied Piper Payments",
            "logo": "http://www.piedpiper.com/app/themes/joystick-v27/images/logo.png",
        }

    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response_data = response.json()
        return response(response_data)
    
    except requests.exceptions.RequestException as err:
        print("The payment didn't go through")
        return Response({"error": str(err)}, status=500)










class CategoryViewset(ModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewset(ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description', 'price']
    ordering_fields = ['price']
    pagination_class = PageNumberPagination


class ProductImageViewset(ModelViewSet):
    pass

class ReviewViewset(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return models.Review.objects.filter(product_id= self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {
            "product_id": self.kwargs['product_pk'],
            'name': self.request.user
            }
    
class CartViewset(CreateModelMixin, RetrieveModelMixin, GenericViewSet, DestroyModelMixin):
    queryset = models.Cart.objects.all()
    serializer_class = CartSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    

class CartItemViewsert(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        return models.CartItem.objects.filter(cart_id = self.kwargs['carts_pk'])
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        
        return CartItemSerializer
            
    def get_serializer_context(self):
        return {
            'cart_id': self.kwargs['carts_pk']
        }

class ProfileViewset(ModelViewSet):
    queryset = models.Profile.objects.all()
    serializer_class = ProfileSerializer
    parser_classes = [MultiPartParser, FormParser]
    

    def create(self, request, *args, **kwargs):
        name = request.data['name']
        bio = request.data['bio']
        picture = request.data['picture']

        models.Profile.objects.create(name=name, bio=bio, picture=picture)
        
        return Response("Profile created succesfully.", status=status.HTTP_200_OK)
    

class OrderViewset(ModelViewSet):

    @action (detail=True, methods=['POST'])
    def pay(self, request, pk):
        order = self.get_object()
        amount = order.total_price
        email = 'ogunkoyamayowa77@gmail.com'
        order_id = str(order.id)
       # redirect_url = "http://127.0.0.1.8000/confirm"
        return initiate_payment(amount, email, order_id)
    
    @action(detail=False, methods=['POST'])
    def confirm_payment(self, request):
        order_id = request.GET.get("o_id")
        order = models.OrderProduct.objects.get(id=order_id)
        order.status = 'deliverd'
        order.save()
        serializer = OrderProductSerializer(order)
        

        data = {
            "message": "Payment was succesful",
            "data": serializer.data
        }
        return Response(data)


    serializer_class = OrderProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return models.OrderProduct.objects.all()
        
        else:
            return models.OrderProduct.objects.filter(user=user)
        
    def get_serializer_class(self):
        
        if self.request.method == 'POST':
            return CreateOrderSerializer
        return OrderProductSerializer


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}


class OrderItemViewset(ModelViewSet):
    queryset = models.OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]
    

