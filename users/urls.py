from django.contrib.auth.decorators import login_required
from django.urls import path

from users.views import UserProfileView, log_in, registration, check_user_exists, check_email_exists, check_user_credentials, logout

app_name = 'users'

urlpatterns = [
    path('profile/<int:pk>/', login_required(UserProfileView.as_view()), name='profile'),
    path('login/', log_in, name='log_in'),
    path('logout/', logout, name='logout'),
    path('registration/', registration, name='registration'),
    path('check_user_exists/', check_user_exists, name='check_username'),
    path('check_email_exists/', check_email_exists, name='check_email'),
    path('check_user_credentials/', check_user_credentials, name='check_email'),
]
