from django.forms import ModelForm

from task_list.models import Task


class TaskUpdateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(TaskUpdateForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'assigned']




