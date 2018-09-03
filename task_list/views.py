from django.http import HttpResponseRedirect
from django.utils import timezone
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.shortcuts import render_to_response
from django.template import RequestContext
from task_list.forms import TaskCreateForm
from task_list.models import Task


class TaskList(ListView):
    model = Task
    ordering = '-created'


class TaskCreate(CreateView):
    model = Task
    form_class = TaskCreateForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create a new '
        context['button'] = 'Add'
        return super().get_context_data(**context)

    def get_form(self, form_class=None):
        return TaskCreateForm(initial={'assigned': self.request.user.pk})

    def post(self, request, *args, **kwargs):
        form = TaskCreateForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            if 'status' in form.changed_data and form.cleaned_data['status'] is True:
                obj.done_by = request.user
                obj.done_date = timezone.now()
            obj.save()
            return HttpResponseRedirect(self.success_url)
        else:
            return self.form_invalid(form)


class TaskDetail(DetailView):
    model = Task
    success_url = '/'


class PostMixin:
    """
    mixin to post method which will process writing and clear a user who mark task 'done'
    """

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        form = self.get_form()
        if form.is_valid():
            if 'status' in form.cleaned_data:
                if form.cleaned_data['status'] is True:
                    # will write a user who make mark done
                    obj.done_by = request.user
                    obj.done_date = timezone.now()
                else:
                    obj.done_by = None
                    obj.done_date = None
            obj.save()
            return super().post(request, *args, **kwargs)
        else:
            return self.form_invalid(form)


class TaskUpdate(PostMixin, UpdateView):
    model = Task
    fields = ['name', 'description', 'status', ]
    success_url = '/'
    template_name = 'task_list/task_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit'
        context['button'] = 'Save'
        return super().get_context_data(**context)

    def get_queryset(self):  # only owner can edit task
        return self.model.objects.filter(assigned=self.request.user)


class TaskDone(PostMixin, UpdateView):
    model = Task
    template_name = 'task_list/task_form.html'
    fields = ['status', ]
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Mark task done'
        context['button'] = 'Save'
        return super().get_context_data(**context)


class TaskDelete(DeleteView):
    model = Task
    success_url = '/'

    def get_queryset(self):  # only owner can delete task
        return self.model.objects.filter(assigned=self.request.user)




def handler404(request, exception, template_name='404.html'):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler500(request, exception, template_name='500.html'):
    response = render_to_response('500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response
