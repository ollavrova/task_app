from django.contrib import admin
from django.utils import timezone

from task_list.models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status', 'created', 'assigned',)

    # def save_model(self, request, obj, form, change):
    #     if not obj.id:
    #         obj.assigned = request.user
    #     if 'status' in form.changed_data and form.changed_data['status'] is True:
    #         obj.done_by = request.user
    #         obj.done_date = timezone.now()
    #     super(TaskAdmin, self).save_model(request, obj, form, change)


admin.site.register(Task, TaskAdmin)
