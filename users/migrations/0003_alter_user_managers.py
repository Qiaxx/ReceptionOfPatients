# Generated by Django 5.2 on 2025-05-06 07:36

import users.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_user_phone_alter_user_email"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="user",
            managers=[
                ("objects", users.models.UserManager()),
            ],
        ),
    ]
