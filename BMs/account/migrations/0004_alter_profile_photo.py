# Generated by Django 4.2.14 on 2024-10-11 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_following'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, default='defaults/default_avatar.jpg', upload_to='users/%Y/%m/%d/'),
        ),
    ]