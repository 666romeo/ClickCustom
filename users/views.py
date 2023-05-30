from django.contrib import auth
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.http import HttpResponse
from common.views import TitleMixin
from users.forms import UserLoginForm, UserProfileForm, UserRegistrationForm
from users.models import User
from django.contrib.auth import authenticate, login


class UserLoginView(LoginView):
    form_class = UserLoginForm
    print(form_class)


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
    return redirect(request.META.get('HTTP_REFERER'))
