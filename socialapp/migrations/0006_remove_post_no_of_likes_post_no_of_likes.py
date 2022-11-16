# Generated by Django 4.1 on 2022-10-31 04:08

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialapp', '0005_remove_post_no_of_likes_post_no_of_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='no_of_likes',
        ),
        migrations.AddField(
            model_name='post',
            name='no_of_likes',
            field=models.ManyToManyField(related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
    ]