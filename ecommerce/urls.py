from ecommerce.views import home
from django.urls import path

urlpatterns = [
    path('', home),
]