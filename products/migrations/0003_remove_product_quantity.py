# Generated by Django 3.2.19 on 2023-07-04 23:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_productimages'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='quantity',
        ),
    ]
