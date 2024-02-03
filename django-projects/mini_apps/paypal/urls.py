

from django.urls import path
from paypal import views


urlpatterns = [
    path('create_payment/', views.create_payment),
    path('capture_payment/', views.capture_payment),
]