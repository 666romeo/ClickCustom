from django.contrib.auth.decorators import login_required
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from users.views import UserProfileView, UserProfileEdit, WorkshopView, log_in, registration, check_user_exists, check_email_exists, check_user_credentials, logout

app_name = 'users'

urlpatterns = [
    path('profile/<int:pk>/', UserProfileView.as_view(), name='profile'),
    path('profile/edit/<int:pk>/', UserProfileEdit.as_view(), name='profile_edit'),
    path('workshop/myproducts/', WorkshopView.as_view(), name='workshop'),
    path('login/', log_in, name='log_in'),
    path('logout/', logout, name='logout'),
    path('registration/', registration, name='registration'),
    path('profile/check_user_exists/', check_user_exists, name='check_username'),
    path('profile/check_email_exists/', check_email_exists, name='check_email'),
    path('profile/check_user_credentials/', check_user_credentials, name='check_credentials'),
]
