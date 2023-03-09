# Generated by Django 4.1.7 on 2023-03-09 04:16

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ("diaryapp", "0002_profile"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Diary",
        ),
        migrations.AlterModelManagers(
            name="user",
            managers=[
                ("obejects", django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name="user",
            name="gender",
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="user",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(max_length=10, unique=True),
        ),
        migrations.DeleteModel(
            name="Profile",
        ),
    ]