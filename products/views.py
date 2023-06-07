from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.shortcuts import HttpResponseRedirect, redirect, render
from django.urls import reverse, reverse_lazy
from django.template.context_processors import request
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views import View
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth import authenticate, login
from common.views import TitleMixin
from products.models import Product, ProductCategory
from django.shortcuts import get_object_or_404, redirect
from users.models import RecentlyViewed, User



class IndexListView(TitleMixin, ListView):
    model = Product
    template_name = 'products/index.html'
    title = 'ClickCustom - Каталог'

    def get_queryset(self):
        queryset = super(IndexListView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(IndexListView, self).get_context_data()
        context['categories'] = ProductCategory.objects.all()
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
        print(recent_items.values_list('product_id', flat=True))
        if product_id in recent_items.values_list('product_id', flat=True):
            recent_items.filter(product_id=product_id).delete()
        print(recent_items.values_list('product_id', flat=True))
        RecentlyViewed.objects.create(user=self.request.user, product=product)
        return Product.objects.filter(id=product_id)


class AboutView(TitleMixin, TemplateView):
    template_name = 'products/about.html'
    title = 'ClickCustom - О нас'


class ConfidentView(TitleMixin, TemplateView):
    template_name = 'products/confident.html'
    title = 'ClickCustom - Политика конфиденциальности'


class OfertaView(TitleMixin, TemplateView):
    template_name = 'products/oferta.html'
    title = 'ClickCustom - Оферта'