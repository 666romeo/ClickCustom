from django.urls import path

from products.views import IndexListView, DetailProductView, AboutView, ConfidentView, OfertaView

app_name = 'product'

urlpatterns = [
    path('', IndexListView.as_view(), name='index'),
    path('product/<int:pk>/', DetailProductView.as_view(), name='product'),
    path('about/', AboutView.as_view(), name='about'),
    path('confident/', ConfidentView.as_view(), name='confident'),
    path('oferta/', OfertaView.as_view(), name='oferta'),
]

