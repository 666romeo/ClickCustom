from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.shortcuts import HttpResponseRedirect, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views import View
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth import authenticate, login
from common.views import TitleMixin
from products.models import Product, ProductCategory
from django.shortcuts import get_object_or_404, redirect
from users.models import RecentlyViewed, User, UserProductsFavorite
from django.http import JsonResponse


class IndexListView(TitleMixin, ListView):
    model = Product
    template_name = 'products/index.html'
    title = 'ClickCustom - Каталог'

    def get_queryset(self):
        queryset = super(IndexListView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ProductCategory.objects.all()
        if str(self.request.user.id) != 'None':
            context['favorite_product_ids'] = UserProductsFavorite.objects.filter(user=self.request.user).values_list(
                'product_id', flat=True)
        return context


class DetailProductView(TitleMixin, ListView):
    model = Product
    template_name = 'products/product.html'
    title = 'ClickCustom - Личный кабинет'

    def get_queryset(self, *args, **kwargs):
        product_id = self.kwargs['pk']
        product = get_object_or_404(Product, pk=product_id)
        recent_items = RecentlyViewed.objects.filter(user=self.request.user.id).order_by('-timestamp')
        max_items = 5

        if recent_items.count() >= max_items:
            oldest_timestamp = recent_items[max_items - 1].timestamp
            recent_items.exclude(timestamp__gte=oldest_timestamp).delete()
        if product_id in recent_items.values_list('product_id', flat=True):
            recent_items.filter(product_id=product_id).delete()
        RecentlyViewed.objects.create(user=self.request.user, product=product)
        return Product.objects.filter(id=product_id)


class UserFavoritesView(TitleMixin, ListView):
    model = UserProductsFavorite
    template_name = 'products/favorites.html'
    title = 'ClickCustom - Избранное'

    def get(self, request, *args, **kwargs):
        user = request.user
        favorite_products = UserProductsFavorite.objects.filter(user=user)
        context = {
            'favorite_products': favorite_products,
        }
        return render(request, self.template_name, context)



def addProductToFavorite(request):
    product_id = request.GET.get('id', None)
    product = get_object_or_404(Product, pk=product_id)
    UserProductsFavorite.objects.create(product=product, user=request.user)
    data = {
        'id_exist': Product.objects.filter(id=product_id).exists()
    }
    return JsonResponse(data)


def removeProductFromFavorite(request):
    product_id = request.GET.get('id', None)
    product = get_object_or_404(Product, pk=product_id)
    favorite_product = UserProductsFavorite.objects.filter(product=product, user=request.user)
    if favorite_product.exists():
        favorite_product.delete()
    data = {
        'id_exist': Product.objects.filter(id=product_id).exists()
    }
    return JsonResponse(data)


class AboutView(TitleMixin, TemplateView):
    template_name = 'products/about.html'
    title = 'ClickCustom - О нас'


class ConfidentView(TitleMixin, TemplateView):
    template_name = 'products/confident.html'
    title = 'ClickCustom - Политика конфиденциальности'


class OfertaView(TitleMixin, TemplateView):
    template_name = 'products/oferta.html'
    title = 'ClickCustom - Оферта'
