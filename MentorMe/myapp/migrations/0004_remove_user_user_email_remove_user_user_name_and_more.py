# Generated by Django 5.1.7 on 2025-03-15 20:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0003_alter_user_user_email"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="user_email",
        ),
        migrations.RemoveField(
            model_name="user",
            name="user_name",
        ),
        migrations.RemoveField(
            model_name="user",
            name="user_password",
        ),
    ]
