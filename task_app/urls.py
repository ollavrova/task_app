"""task_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from task_list import views
from task_list.views import TaskDetail, TaskUpdate, TaskDelete, TaskCreate, TaskDone
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('', views.TaskList.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(), {'template_name': 'login.html'}, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('tasks/detail/<int:pk>/', login_required(TaskDetail.as_view()), name='task-detail'),
    path('tasks/edit/<int:pk>/', login_required(TaskUpdate.as_view()), name='task-edit'),
    path('tasks/done/<int:pk>/', login_required(TaskDone.as_view()), name='task-done'),
    path('tasks/delete/<int:pk>/', login_required(TaskDelete.as_view()), name='task-delete'),
    path('tasks/create/', login_required(TaskCreate.as_view()), name='task-create'),

]
