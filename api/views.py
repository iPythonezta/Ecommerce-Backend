from django.conf import settings
from rest_framework import generics, permissions, status
from rest_framework.permissions import AllowAny
from .models import CustomUser, Product, Cart, CartItem, OrderItem, Order
from .serializers import CustomUserSerializer, ProductSerializer, CartSerializer, OrderSerializer
from rest_framework.response import Response


class CustomUserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (AllowAny,)

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

class CartView(generics.RetrieveUpdateAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user = self.request.user
        cart, created = Cart.objects.get_or_create(user=user)
        return cart

    def update(self, request, *args, **kwargs):
        cart = self.get_object()
        action = request.data.get('action')
        product_id = request.data.get('product_id')

        if action == 'add':
            quantity = request.data.get('quantity', 1)
            product = Product.objects.get(pk=product_id)

            # Add or update the item in the cart
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            cart_item.quantity += int(quantity)
            cart_item.save()

        elif action == 'remove':
            try:
                cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
                quantity = request.data.get('quantity', 1)
                if quantity:
                    cart_item.quantity -= int(quantity)
                    if cart_item.quantity <= 0:
                        cart_item.delete()
                    else:
                        cart_item.save()
                else:
                    cart_item.delete()
            except CartItem.DoesNotExist:
                return Response({'detail': 'Item not found in the cart.'}, status=status.HTTP_404_NOT_FOUND)

        else:
            return Response({'detail': 'Invalid action.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(cart)
        return Response(serializer.data)


class OrderView(generics.CreateAPIView, generics.UpdateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user = self.request.user
        order = Order.objects.create(user=user, status=False)
        return order

    def create(self, request, *args, **kwargs):
        cart = self.get_cart()
        if len(cart.cart_items.all()) == 0:
            return Response({'error':'Cart is empty'})
        order = self.get_object()

        # Create order items based on cart items
        order_items = []
        for cart_item in cart.cart_items.all():
            order_item = OrderItem(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                subtotal=cart_item.subtotal()
            )
            order_items.append(order_item)

        OrderItem.objects.bulk_create(order_items)

        # Update order details
        order.total_items = cart.total_items()
        order.total_price = cart.total_price()
        order.save()

        cart.cart_items.all().delete()

        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_cart(self):
        user = self.request.user
        cart, created = Cart.objects.get_or_create(user=user)
        return cart

class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user) if not user.is_superuser else Order.objects.all() 
        # returning all orders if user is a superuser otherwise returning orders belonging to the user only
    

class OrderDetailView(generics.RetrieveAPIView, generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        # Check if the user is the creator of the order or is a superuser
        if request.user == instance.user or request.user.is_superuser:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)

        return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        # Only admin users can update the order status
        if not request.user.is_superuser:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        return super().update(request, *args, **kwargs)