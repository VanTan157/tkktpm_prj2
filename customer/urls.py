from django.urls import path
from .views import CustomerListCreateView, CustomerDetailView, CustomerTokenObtainPairView, UserProfileView

urlpatterns = [
    path('customers/', CustomerListCreateView.as_view(), name='customer-list-create'),
    path('customers/<int:pk>/', CustomerDetailView.as_view(), name='customer-detail'),
    path('login/', CustomerTokenObtainPairView.as_view(), name='customer_token_obtain_pair'),
    path('customers/profile/', UserProfileView.as_view(), name='user-profile'),
]
