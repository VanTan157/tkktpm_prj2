from django.urls import path
from .views import MobileListCreateView, MobileDetailView

urlpatterns = [
    path('mobiles/', MobileListCreateView.as_view(), name='mobile-list-create'),
    path('mobiles/<str:_id>/', MobileDetailView.as_view(), name='mobile-detail'),
]
