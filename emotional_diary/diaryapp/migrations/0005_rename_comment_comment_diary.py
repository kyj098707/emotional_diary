# Generated by Django 4.1.7 on 2023-03-30 04:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("diaryapp", "0004_remove_diary_comment_comment_comment"),
    ]

    operations = [
        migrations.RenameField(
            model_name="comment",
            old_name="comment",
            new_name="diary",
        ),
    ]