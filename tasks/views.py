from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Task
from django.urls import reverse_lazy
from django.utils import timezone
from django.http import HttpResponseForbidden


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    
    def get_queryset(self):
        # Only show tasks created by the logged-in user
        return Task.objects.filter(created_by=self.request.user)

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.created_by != self.request.user:
            return HttpResponseForbidden(f"You do not have the permission to view this Task, Please contact {obj.created_by}")
        return obj

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'tasks/task_form.html'
    fields = ['title', 'description', 'due_date', 'priority', 'status']

    def form_valid(self, form):
        form.instance.created_by = self.request.user  # Set the user who created the task
        return super().form_valid(form)

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = 'tasks/task_form.html'
    fields = ['title', 'description', 'due_date', 'priority', 'status']

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.created_by != self.request.user:
            return HttpResponseForbidden(f"You do not have the permission to update this Task, Please contact {obj.created_by}")
        return obj

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('task_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.created_by != self.request.user:
            return HttpResponseForbidden(f"You do not have the permission to delete this Task, Please contact {obj.created_by}")
        return obj

###USER AUTHENTICATION###
from django.contrib.auth import logout

def logout_view(request):
    # Assuming you have set up logout logic
    logout(request)
    return render(request, 'registration/logout.html')