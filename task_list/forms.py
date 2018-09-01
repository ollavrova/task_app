from django.forms import ModelForm
from task_list.models import Task


class TaskCreateForm(ModelForm):

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'assigned']
