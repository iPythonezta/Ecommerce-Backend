from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from .views import OrderListView,OrderDetailView, CustomUserCreateView, ProductCreateView, ProductDetailView, ProductListView, CartView, OrderView

urlpatterns = [
    path('user/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('user/register/', CustomUserCreateView.as_view(), name='register'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/create/', ProductCreateView.as_view(), name='product-create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('cart/', CartView.as_view(), name='cart-detail'),
    path('cart/order/', OrderView.as_view(), name='order'),
    path('orders/', OrderListView.as_view(), name='order-details'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
]