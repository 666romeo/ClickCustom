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
from django.core.files.storage import default_storage
from django.forms import modelformset_factory
from django.http import HttpResponse
import os
import re
from urllib.parse import unquote

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


class EditProductView(TitleMixin, ListView):
    model = Product
    form_class = ProductImagesForm
    template_name = 'products/edit_product.html'
    title = 'ClickCustom - Редактор товара'

    def get_context_data(self, **kwargs):
        form = self.form_class()
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
        context['product_id'] = product_id
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        product_id = self.kwargs['pk']
        product = get_object_or_404(Product, pk=product_id)
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.description = request.POST.get('description')
        new_image = request.POST.get('main_image')
        new_image = new_image.replace('/media/', '')
        product.image = new_image
        product.save()

        return HttpResponse(status=200)

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
        images = [unquote(image.image.url) for image in images]
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
    categoryEnToRu = {'clothes': 'Одежда',
                      'shoes': 'Обувь',
                      'accessories': 'Аксессуары',
                      'other': 'Другое'}
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
        desired_value = request.POST.get('category')
        category_name = next(key for key, value in self.categoryEnToRu.items() if value == desired_value)
        category = get_object_or_404(ProductCategory, name=category_name)
        name = request.POST.get('name')
        price = int(request.POST.get('price'))
        description = request.POST.get('description')
        image = request.FILES.getlist('image')
        images = request.FILES.getlist('images')
        main_image_name = image[0].name

        product = Product.objects.create(
            name=name,
            price=price,
            category=category,
            description=description,
            image=image[0],
        )

        # Создаем объекты ProductImages только для остальных файлов изображений
        for img in images:
            # Пропускаем главное изображение
            if img.name == main_image_name:
                continue

            ProductImages.objects.create(
                product=product,
                image=img,
            )
        ProductImages.objects.create(
            product=product,
            image=product.image.url.replace('media/', ''),
        )

        ProductAuthor.objects.create(
            product=product,
            author=user,
        )

        # Перенаправляем пользователя на страницу успешного создания товара
        return redirect('index')

def add_images_to_product(request, product_id):
    if request.method == 'POST' and request.FILES.getlist('images'):
        product = get_object_or_404(Product, pk=product_id)
        image_extensions = ['.jpg', '.jpeg', '.png']
        images = [image for image in request.FILES.getlist('images') if os.path.splitext(image.name)[1].lower() in image_extensions]
        for image in images:
            ProductImages.objects.create(product=product, image=image)
        product_images = ProductImages.objects.filter(product=product_id)
        image_urls = [unquote(image.image.url) for image in product_images]
        data = {'images': image_urls}
        return JsonResponse(data)
    return JsonResponse({'error': 'Неверный запрос или отсутствуют изображения.'}, status=400)


def delete_images(request, product_id):
    if request.method == 'POST':
        deleted_slides = request.POST.getlist('deleted_slides[]')
        for i in deleted_slides:
            ProductImages.objects.filter(image=i.replace('/media/', '')).delete()
        return HttpResponse(status=200)

def delete_image(request, product_id):
    if request.method == 'GET':
        product = get_object_or_404(Product, pk=product_id)
        images = ProductImages.objects.filter(product=product)
        image_urls = [image.image.url for image in images]
        return JsonResponse({'images': image_urls})

    elif request.method == 'POST':
        image_id = int(request.POST.get('image_id'))
        # Удаление изображения из базы данных

        images = ProductImages.objects.filter(product=Product.objects.get(id=product_id))
        image = images[image_id]
        image_path = image.image.path
        if default_storage.exists(image_path):
            default_storage.delete(image_path)
        image.delete()
        return JsonResponse({'images': ProductImages.objects.filter(product=Product.objects.get(id=product_id))})

def assign_main_photo(request, product_id):
    if request.method == 'POST':
        new_image = request.POST.get('new_image')
        new_image = new_image.replace('/media/', '')
        product = Product.objects.get(pk=product_id)
        product.image = new_image
        product.save()
        data = {
            'images': Product.objects.get(pk=product_id).image.url
        }
        return JsonResponse(data)

def delete_product(request):
    if request.method == 'POST':
        product_id = request.POST.get('pk')
        product = Product.objects.filter(pk=product_id)
        product.delete()
        data = {
            'delete': 'True'
        }
        return JsonResponse(data)

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
