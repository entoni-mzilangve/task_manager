# Generated by Django 4.2 on 2024-08-23 23:40

from django.db import migrations, models
import main.services.storage_backends


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0005_user_date_of_birth_user_phone"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="avatar_picture",
            field=models.ImageField(
                null=True,
                storage=main.services.storage_backends.public_storage,
                upload_to="",
            ),
        ),
    ]
