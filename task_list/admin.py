from django.contrib import admin

from task_list.models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created', 'assigned',)


admin.site.register(Task, TaskAdmin)