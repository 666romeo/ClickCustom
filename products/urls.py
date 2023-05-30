from django.urls import path

from products.views import IndexListView, DetailProductView

app_name = 'products'

urlpatterns = [
    path('', IndexListView.as_view(), name='index'),
    path('product/<int:pk>/', DetailProductView.as_view(), name='product'),
]

