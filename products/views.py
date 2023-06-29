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
from products.models import Product, ProductCategory, ProductImages
from users.models import ProductAuthor
from django.shortcuts import get_object_or_404, redirect
from users.models import RecentlyViewed, User, UserProductsFavorite
from django.http import JsonResponse
from products.forms import ProductImagesForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from PIL import Image
from utils.remove_background import remove_background


class IndexListView(TitleMixin, ListView):
    model = Product
    template_name = 'products/index.html'
    title = 'ClickCustom - Каталог'

    def get_queryset(self):
        queryset = super(IndexListView, self).get_queryset()
        category_name = self.kwargs.get('category_name')
        if category_name:
            category = ProductCategory.objects.get(name=category_name)
            queryset = queryset.filter(category=category)
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price and max_price:
            queryset = queryset.filter(price__gte=min_price, price__lte=max_price)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        categoryEnToRu = {'clothes': 'Одежда',
                          'shoes': 'Обувь',
                          'accessories': 'Аксессуары',
                          'other': 'Другое'}
        context['categories'] = ProductCategory.objects.all()
        context['category_name'] = categoryEnToRu.get(str(self.kwargs.get('category_name')))
        if str(self.request.user.id) != 'None':
            context['favorite_product_ids'] = UserProductsFavorite.objects.filter(user=self.request.user).values_list(
                'product_id', flat=True)
        return context


class DetailProductView(TitleMixin, ListView):
    model = Product
    template_name = 'products/product.html'
    title = 'ClickCustom - Личный кабинет'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = self.kwargs['pk']
        recent_items = RecentlyViewed.objects.filter(user=self.request.user.id).order_by('-timestamp')
        max_items = 5

        if recent_items.count() >= max_items:
            oldest_timestamp = recent_items[max_items - 1].timestamp
            recent_items.exclude(timestamp__gte=oldest_timestamp).delete()
        if product_id in recent_items.values_list('product_id', flat=True):
            recent_items.filter(product_id=product_id).delete()
        RecentlyViewed.objects.create(user=self.request.user, product=get_object_or_404(Product, pk=product_id))

        product = Product.objects.filter(id=product_id)
        images = ProductImages.objects.filter(product=Product.objects.get(id=product_id))
        author = ProductAuthor.objects.get(product=Product.objects.get(id=product_id))
        context['product'] = product
        context['images'] = images
        context['author'] = author.author
        return context


class UserFavoritesView(TitleMixin, LoginRequiredMixin, ListView):
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


class CreateProductView(TitleMixin, LoginRequiredMixin, CreateView):
    form_class = ProductImagesForm
    template_name = 'products/workshop.html'
    title = 'ClickCustom - Workshop'

    def get(self, request, *args, **kwargs):
        user = request.user
        form = self.form_class()
        context = {
            'user': user,
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user = request.user
        form = self.form_class(request.POST, request.FILES)

        # Создаем новый товар
        category_name = request.POST.get('category')
        category = get_object_or_404(ProductCategory, name=category_name)
        name = request.POST.get('name')
        price = int(request.POST.get('price'))
        description = request.POST.get('description')
        image = request.FILES.get('image')
        # Сохраняем товар в базе данных
        product = Product.objects.create(
            name=name,
            price=price,
            category=category,
            description=description,
            image=image,
        )

        # Создаем объекты ProductImages для каждой загруженной фотографии
        images = request.FILES.getlist('images')
        for img in images:
            ProductImages.objects.create(
                product=product,
                image=img,
            )

        ProductAuthor.objects.create(
            product=product,
            author=user,
        )

        # Перенаправляем пользователя на страницу успешного создания товара
        return redirect('index')


def remove_background_view(request):
    if request.method == 'POST':
        # Получение загруженного файла из запроса
        uploaded_file = request.FILES['image']

        # Удаление фона и получение закодированного изображения
        encoded_image = remove_background(uploaded_file)
        data = {
            'encoded_image': encoded_image
        }
        return JsonResponse(data)

    data = {
        'error': 'error'
    }
    return JsonResponse(data)

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
