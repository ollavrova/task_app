from django.utils import timezone
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.shortcuts import render_to_response
from django.template import RequestContext
from task_list.forms import TaskUpdateForm
from task_list.models import Task


class TaskList(ListView):
    model = Task
    ordering = '-created'


class TaskCreate(CreateView):
    model = Task
    success_url = '/'
    fields = ['name', 'description', 'status', 'assigned']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create a new '
        context['button'] = 'Add'
        return super().get_context_data(**context)

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        form = self.get_form()
        if form.is_valid():
            if not obj.id:
                obj.assigned = request.user
            if 'status' in form.changed_data and form.cleaned_data['status'] is True:
                obj.done_by = request.user
                obj.done_date = timezone.now()
                obj.save()
            return self.form_valid(form)
        return super().post(request, *args, **kwargs)


class TaskDetail(DetailView):
    model = Task
    success_url = '/'
    template_name = 'task_list/task_detail.html'


class TaskUpdate(UpdateView):
    model = Task
    form_class = TaskUpdateForm
    success_url = '/'
    template_name = 'task_list/task_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit '
        context['button'] = 'Save'
        return super().get_context_data(**context)

    def get_queryset(self):  # only owner can edit task
        return self.model.objects.filter(assigned=self.request.user)

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        form = self.get_form()
        if form.is_valid():
            if 'status' in form.changed_data and form.cleaned_data['status'] is True:
                obj.done_by = request.user
                obj.done_date = timezone.now()
                obj.save()
            return self.form_valid(form)
        return super().post(request, *args, **kwargs)


class TaskDone(UpdateView):
    model = Task
    template_name = 'task_list/make_done.html'
    fields = ['status']
    success_url = '/'

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        form = self.get_form()
        if form.is_valid():
            if 'status' in form.changed_data and form.cleaned_data['status'] is True:
                obj.done_by = request.user
                obj.done_date = timezone.now()
                obj.save()
            return self.form_valid(form)
        return super().post(request, *args, **kwargs)


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
