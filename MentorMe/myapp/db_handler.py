import re
from django.core.exceptions import PermissionDenied
from django.db import models
from django.contrib.auth import get_user_model
from .models import User, Subject, LogType, Log, Advertisement, Class

class DBHandler:
    """
    Клас для взаємодії з базою даних, включає базові CRUD операції (створення, читання, оновлення, видалення)
    з додатковими перевірками на безпеку та права доступу.
    """
    def __init__(self, user):
        self.user = user

    def check_for_injections(self, query):
        """ Перевіряє SQL-запити на наявність потенційно небезпечних ін'єкцій """
        dangerous_patterns = [
            r";--", r"--", r";", r"\b(OR|AND)\b.*\b(=|LIKE)\b", 
            r"UNION.*SELECT", r"DROP TABLE", r"ALTER TABLE", 
            r"INSERT INTO", r"DELETE FROM"
        ]
        for pattern in dangerous_patterns:
            if re.search(pattern, query, re.IGNORECASE):
                raise ValueError("Запит містить потенційну SQL-ін'єкцію.")

    def check_user_permissions(self, action):
        """ Перевіряє права користувача на виконання операції """
        if not self.user.is_authenticated:
            raise PermissionDenied("Користувач не автентифікований.")
        
        if action not in ['read', 'write', 'update', 'delete']:
            raise ValueError("Невідомий тип операції.")
        
        if action in ['write', 'update', 'delete'] and self.user.user_def_role != 'Admin':
            raise PermissionDenied("Недостатньо прав для виконання операції.")

    def write(self, model, data):
        """ Додає новий запис у базу даних """
        self.check_user_permissions('write')
        if not issubclass(model, models.Model):
            raise ValueError("Переданий об'єкт не є моделлю Django.")
        instance = model.objects.create(**data)
        return instance

    def read(self, model, filters=None):
        """ Читає записи з бази даних з можливістю фільтрації """
        self.check_user_permissions('read')
        if not issubclass(model, models.Model):
            raise ValueError("Переданий об'єкт не є моделлю Django.")
        
        query = model.objects.all()
        if filters:
            query = query.filter(**filters)
        return query

    def update(self, model, filters, update_data):
        """ Оновлює записи в базі даних """
        self.check_user_permissions('update')
        if not issubclass(model, models.Model):
            raise ValueError("Переданий об'єкт не є моделлю Django.")
        
        updated_count = model.objects.filter(**filters).update(**update_data)
        return updated_count

    def delete(self, model, filters):
        """ Видаляє записи з бази даних """
        self.check_user_permissions('delete')
        if not issubclass(model, models.Model):
            raise ValueError("Переданий об'єкт не є моделлю Django.")
        
        deleted_count, _ = model.objects.filter(**filters).delete()
        return deleted_count