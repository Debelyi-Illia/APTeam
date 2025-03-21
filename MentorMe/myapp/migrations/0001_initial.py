# Generated by Django 5.1.7 on 2025-03-11 17:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LogType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lt_name', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_name', models.CharField(max_length=150)),
                ('sub_description', models.TextField(blank=True, null=True)),
                ('sub_color', models.CharField(blank=True, max_length=7, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=150)),
                ('user_real_name', models.CharField(max_length=150)),
                ('user_password', models.CharField(max_length=150)),
                ('user_email', models.EmailField(max_length=254, unique=True)),
                ('user_phone', models.CharField(blank=True, max_length=20, null=True)),
                ('user_biography', models.TextField(blank=True, null=True)),
                ('user_def_hours', models.IntegerField(default=0)),
                ('user_def_role', models.CharField(max_length=50)),
                ('user_def_subject', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='myapp.subject')),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('log_text_body', models.TextField()),
                ('log_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.logtype')),
                ('log_receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.user')),
            ],
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cl_hours', models.BigIntegerField()),
                ('cl_completed', models.BooleanField(default=False)),
                ('cl_planned', models.BooleanField(default=True)),
                ('cl_name', models.CharField(max_length=150)),
                ('cl_subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.subject')),
                ('cl_student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_classes', to='myapp.user')),
                ('cl_teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teacher_classes', to='myapp.user')),
            ],
        ),
        migrations.CreateModel(
            name='Advertisement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ad_hours', models.IntegerField()),
                ('ad_role', models.BooleanField()),
                ('ad_name', models.CharField(max_length=150)),
                ('ad_text_body', models.TextField()),
                ('ad_subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.subject')),
                ('ad_poster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.user')),
            ],
        ),
    ]
