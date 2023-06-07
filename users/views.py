from django.contrib import auth
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.http import HttpResponse
from common.views import TitleMixin
from users.forms import UserProfileForm
from users.models import User, RecentlyViewed, UserProductsFavorite
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views import View
import os
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse, HttpResponseForbidden


class UserProfileEdit(TitleMixin, LoginRequiredMixin, View):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile_edit.html'
    title = 'ClickCustom - Личный кабинет'

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs['pk']
        if request.user.id != user_id:
            # Если текущий пользователь не соответствует запрошенному профилю
            return redirect('/profile/{}/edit'.format(request.user.id))

        user = User.objects.get(id=user_id)
        form = self.form_class()
        context = {
            'user': user,
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user_id = self.kwargs['pk']
        if request.user.id != user_id:
            # Если текущий пользователь не соответствует запрошенному профилю
            # Вы можете вернуть ошибку 403 Forbidden или перенаправить на другую страницу
            return HttpResponseForbidden("Вы не имеете доступа к этому профилю.")

        user = User.objects.get(id=user_id)
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            # Удаление предыдущего изображения пользователя
            if user.image and 'image' in request.FILES:
                self.delete_previous_image(user.image.path, user)

            # Сохранение нового изображения пользователя
            image = form.cleaned_data['image']
            if image:
                user.image = image
                user.save()

        context = {
            'user': user,
            'form': form,
        }
        return render(request, self.template_name, context)

    def delete_previous_image(self, image_path, user):
        if os.path.isfile(image_path):
            os.remove(image_path)
            user.image = None
            user.save()


class UserProfileView(TitleMixin, LoginRequiredMixin, View):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    title = 'ClickCustom - Личный кабинет'

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs['pk']
        user = User.objects.get(id=user_id)
        form = self.form_class()
        recently_viewed = RecentlyViewed.objects.filter(user=user).order_by('-timestamp')
        context = {
            'user': user,
            'form': form,
            'recently_viewed': recently_viewed[:5],
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user_id = self.kwargs['pk']
        if request.user.id != user_id:
            return HttpResponseForbidden("Вы не имеете доступа к этому профилю.")

        user = User.objects.get(id=user_id)
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            # Удаление предыдущего изображения пользователя
            if user.image and 'image' in request.FILES:
                self.delete_previous_image(user.image.path, user)

            # Сохранение нового изображения пользователя
            image = form.cleaned_data['image']
            if image:
                user.image = image
                user.save()

        context = {
            'user': user,
            'form': form,
        }
        return render(request, self.template_name, context)

    def delete_previous_image(self, image_path, user):
        if os.path.isfile(image_path):
            os.remove(image_path)
            # Обновление поля изображения пользователя
            user.image = None
            user.save()


def logout(request):
    auth.logout(request)
    return redirect('index')


def registration(request):
    email = request.POST.get('email')
    username = request.POST.get('username')
    password = request.POST.get('password')
    confirm_password = request.POST.get('confirm_password')
    if not username or not password or not confirm_password or not email:
        return redirect(request.META.get('HTTP_REFERER'))
    if password != confirm_password:
        return redirect(request.META.get('HTTP_REFERER'))
    User.objects.create_user(username=username, password=password, email=email)
    user = authenticate(request, username=username, password=password)
    login(request, user)
    return redirect('users:profile', user.id)


def log_in(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect(request.META.get('HTTP_REFERER'))


def check_user_exists(request):
    email = request.GET.get('email', None)
    username = request.GET.get('username', None)
    data = {
        'email_taken': User.objects.filter(email=email).exists(),
        'username_taken': User.objects.filter(username=username).exists()
    }
    return JsonResponse(data)


def check_email_exists(request):
    email = request.GET.get('email', None)
    data = {
        'email_taken': User.objects.filter(email=email).exists(),
    }
    return JsonResponse(data)


def check_user_credentials(request):
    username = request.GET.get('username')
    password = request.GET.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        return JsonResponse({'credentials_valid': True})
    else:
        return JsonResponse({'credentials_valid': False})