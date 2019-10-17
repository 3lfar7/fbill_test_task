from django.urls import path
from .views import RequestAmountView

urlpatterns = [
    path('request/<int:amount>/', RequestAmountView.as_view())
]