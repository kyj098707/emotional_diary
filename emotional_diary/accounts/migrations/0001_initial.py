# Generated by Django 4.1.7 on 2023-03-29 10:47

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                ("username", models.CharField(max_length=10, unique=True)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("nickname", models.CharField(max_length=10)),
                ("is_active", models.BooleanField(default=False)),
                ("is_admin", models.BooleanField(default=False)),
                ("is_superuser", models.BooleanField(default=False)),
                ("is_staff", models.BooleanField(default=False)),
                (
                    "follower",
                    models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
