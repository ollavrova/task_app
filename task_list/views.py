from django.views.generic import TemplateView
from task_list.models import Task


class Home(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['tasks'] = Task.objects.order_by('-created').all()
        return context
