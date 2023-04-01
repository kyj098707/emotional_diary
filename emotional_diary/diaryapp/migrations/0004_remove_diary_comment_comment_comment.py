# Generated by Django 4.1.7 on 2023-03-30 04:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("diaryapp", "0003_remove_comment_diary_diary_comment"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="diary",
            name="comment",
        ),
        migrations.AddField(
            model_name="comment",
            name="comment",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="diaryapp.diary",
            ),
        ),
    ]