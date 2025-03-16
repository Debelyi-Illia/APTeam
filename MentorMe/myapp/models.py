from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# Модель користувача, що розширює AbstractUser
class User(AbstractUser):
    user_real_name = models.CharField(max_length=150) # Реальне ім'я користувача
    user_phone = models.CharField(max_length=20, blank=True, null=True) # Номер телефону
    user_biography = models.TextField(blank=True, null=True) # Біографія
    user_def_hours = models.IntegerField(default=0) # Години, коли користувач може викладати/займатися
    user_def_role = models.CharField(max_length=50)  # Роль користувача (наприклад, вчитель, студент)
    user_def_subject = models.ForeignKey('Subject', on_delete=models.SET_NULL, null=True) # Предмет

# Модель предмету (дисципліни)
class Subject(models.Model):
    sub_name = models.CharField(max_length=150) # Назва предмету
    sub_description = models.TextField(blank=True, null=True)  # Опис предмету
    sub_color = models.CharField(max_length=7, blank=True, null=True)  # Колір предмету у HEX форматі

# Модель типу логів
class LogType(models.Model):
    lt_name = models.CharField(max_length=150) # Назва типу логу

# Модель логування подій
class Log(models.Model):
    log_type = models.ForeignKey(LogType, on_delete=models.CASCADE) # Тип логу
    log_receiver = models.ForeignKey(User, on_delete=models.CASCADE) # Користувач, що отримав запис у лог
    log_text_body = models.TextField() # Текст логу

# Модель оголошень
class Advertisement(models.Model):
    ad_poster = models.ForeignKey(User, on_delete=models.CASCADE) # Користувач, що створив оголошення
    ad_start_time = models.DateTimeField(default=timezone.now) # Час закінчення дії оголошення
    ad_end_time = models.DateTimeField() # Час закінчення дії оголошення
    ad_role = models.CharField(max_length=150) # Цільова роль оголошення
    ad_subject = models.CharField(max_length=150) # Предмет оголошення
    ad_title = models.CharField(max_length=150) # Заголовок оголошення
    ad_text_body = models.TextField() # Текст оголошення
    is_active = models.BooleanField(default=True) # Чи активне оголошення

# Модель класу (уроку)
class Class(models.Model):
    cl_teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teacher_classes') # Викладач
    cl_student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_classes') # Студент
    cl_hours = models.BigIntegerField()  # 168-бітне число для побітового кодування розкладу
    cl_subject = models.ForeignKey(Subject, on_delete=models.CASCADE) # Предмет уроку
    cl_completed = models.BooleanField(default=False) # Чи завершений урок
    cl_planned = models.BooleanField(default=True) # Чи запланований урок
    cl_name = models.CharField(max_length=150) # Назва уроку