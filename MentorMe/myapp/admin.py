from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Subject)
admin.site.register(Log)
admin.site.register(LogType)
admin.site.register(Advertisement)
admin.site.register(Class)