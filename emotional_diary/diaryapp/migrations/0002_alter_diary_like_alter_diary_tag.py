# Generated by Django 4.1.7 on 2023-03-29 10:54

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("diaryapp", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="diary",
            name="like",
            field=models.ManyToManyField(
                blank=True, related_name="like_diary", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterField(
            model_name="diary",
            name="tag",
            field=models.ManyToManyField(
                blank=True, related_name="diary_tag", to="diaryapp.tag"
            ),
        ),
    ]