from django.contrib import admin
from .models import TasksModel, SubTasksModel

admin.site.register(TasksModel)
admin.site.register(SubTasksModel)
