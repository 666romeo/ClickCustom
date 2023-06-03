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
    success_url = reverse_lazy('products:product')
    title = 'ClickCustom - Личный кабинет'

    def get_queryset(self, *args, **kwargs):
        queryset = super(DetailProductView, self).get_queryset()
        product_id = self.kwargs['pk']
        return Product.objects.filter(id=product_id)
