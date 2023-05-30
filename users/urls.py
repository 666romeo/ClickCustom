from django.contrib.auth.decorators import login_required
from django.urls import path

from users.views import UserProfileView, logout

app_name = 'users'

urlpatterns = [
    path('profile/<int:pk>/', login_required(UserProfileView.as_view()), name='profile'),
    path('logout/', logout, name='logout'),
]
