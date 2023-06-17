from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from products.models import Product


class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    town = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username


class RecentlyViewed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)


class UserProductsFavorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class ProductAuthor(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
