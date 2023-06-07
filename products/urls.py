from django.urls import path

from products.views import IndexListView, addProductToFavorite, removeProductFromFavorite, DetailProductView, AboutView, ConfidentView, OfertaView, UserFavoritesView

app_name = 'product'

urlpatterns = [
    path('', IndexListView.as_view(), name='index'),
    path('product/<int:pk>/', DetailProductView.as_view(), name='product'),
    path('favorites/', UserFavoritesView.as_view(), name='favorites'),
    path('about/', AboutView.as_view(), name='about'),
    path('confident/', ConfidentView.as_view(), name='confident'),
    path('oferta/', OfertaView.as_view(), name='oferta'),
    path('add_product_to_favorite/', addProductToFavorite, name='addProductToFavorite'),
    path('remove_product_from_favorite/', removeProductFromFavorite, name='removeProductFromFavorite'),
]

