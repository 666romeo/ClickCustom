from django.urls import path

from products.views import IndexListView, addProductToFavorite, CreateProductView, removeProductFromFavorite, \
    remove_background_view, DetailProductView, AboutView, ConfidentView, OfertaView, UserFavoritesView, EditProductView

app_name = 'product'

urlpatterns = [
    path('', IndexListView.as_view(), name='index'),
    path('category/<str:category_name>/', IndexListView.as_view(), name='index_category'),
    path('product/<int:pk>/', DetailProductView.as_view(), name='product'),
    path('product/edit/<int:pk>/', EditProductView.as_view(), name='product_edit'),
    path('favorites/', UserFavoritesView.as_view(), name='favorites'),
    path('remove_background/', remove_background_view, name='remove_background'),
    path('product/create/', CreateProductView.as_view(), name='createproduct'),
    path('about/', AboutView.as_view(), name='about'),
    path('confident/', ConfidentView.as_view(), name='confident'),
    path('oferta/', OfertaView.as_view(), name='oferta'),
    path('add_product_to_favorite/', addProductToFavorite, name='addProductToFavorite'),
    path('remove_product_from_favorite/', removeProductFromFavorite, name='removeProductFromFavorite'),
]

