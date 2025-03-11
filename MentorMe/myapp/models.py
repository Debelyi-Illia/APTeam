from django.db import models

# Create your models here.
class User(models.Model):
    user_name = models.CharField(max_length=150)
    user_real_name = models.CharField(max_length=150)
    user_password = models.CharField(max_length=150)
    user_email = models.EmailField(unique=True)
    user_phone = models.CharField(max_length=20, blank=True, null=True)
    user_biography = models.TextField(blank=True, null=True)
    user_def_hours = models.IntegerField(default=0)
    user_def_role = models.CharField(max_length=50)
    user_def_subject = models.ForeignKey('Subject', on_delete=models.SET_NULL, null=True)


class Subject(models.Model):
    sub_name = models.CharField(max_length=150)
    sub_description = models.TextField(blank=True, null=True)
    sub_color = models.CharField(max_length=7, blank=True, null=True)  # Hex color code


class LogType(models.Model):
    lt_name = models.CharField(max_length=150)


class Log(models.Model):
    log_type = models.ForeignKey(LogType, on_delete=models.CASCADE)
    log_receiver = models.ForeignKey(User, on_delete=models.CASCADE)
    log_text_body = models.TextField()


class Advertisement(models.Model):
    ad_poster = models.ForeignKey(User, on_delete=models.CASCADE)
    ad_hours = models.IntegerField()
    ad_role = models.BooleanField()  # True for teacher, False for student
    ad_subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    ad_name = models.CharField(max_length=150)
    ad_text_body = models.TextField()


class Class(models.Model):
    cl_teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teacher_classes')
    cl_student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_classes')
    cl_hours = models.BigIntegerField()  # 168-бітне число для побітового кодування
    cl_subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    cl_completed = models.BooleanField(default=False)
    cl_planned = models.BooleanField(default=True)
    cl_name = models.CharField(max_length=150)
