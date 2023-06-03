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
from users.models import User
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login


class UserProfileView(TitleMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')
    title = 'ClickCustom - Личный кабинет'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))


def logout(request):
    auth.logout(request)
    return redirect('index')


def registration(request):
    email = request.POST.get('email')
    username = request.POST.get('username')
    password = request.POST.get('password')
    confirm_password = request.POST.get('confirm_password')
    print(email, username, password, confirm_password)
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
    print(email)
    print(username)
    data = {
        'email_taken': User.objects.filter(email=email).exists(),
        'username_taken': User.objects.filter(username=username).exists()
    }
    print(data)
    return JsonResponse(data)


def check_email_exists(request):
    email = request.GET.get('email', None)
    print(email)
    data = {
        'email_taken': User.objects.filter(email=email).exists(),
    }
    print(data)
    return JsonResponse(data)


def check_user_credentials(request):
    username = request.GET.get('username')
    password = request.GET.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        return JsonResponse({'credentials_valid': True})
    else:
        return JsonResponse({'credentials_valid': False})
