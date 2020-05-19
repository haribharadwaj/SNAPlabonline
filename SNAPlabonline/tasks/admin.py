from django.contrib import admin
from .models import Task, Response

# Register your models here.
admin.site.register(Task)
admin.site.register(Response)