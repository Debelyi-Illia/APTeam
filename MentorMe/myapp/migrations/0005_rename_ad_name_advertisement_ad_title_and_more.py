# Generated by Django 5.1.7 on 2025-03-16 17:01

from django.db import migrations, models
from django.utils import timezone



class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_remove_user_user_email_remove_user_user_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='advertisement',
            old_name='ad_name',
            new_name='ad_title',
        ),
        migrations.RemoveField(
            model_name='advertisement',
            name='ad_hours',
        ),
        migrations.AddField(
            model_name='advertisement',
            name='ad_end_time',
            field=models.DateTimeField(default=timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='advertisement',
            name='ad_start_time',
            field=models.DateTimeField(default=timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='advertisement',
            name='ad_role',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='advertisement',
            name='ad_subject',
            field=models.CharField(max_length=150),
        ),
    ]
