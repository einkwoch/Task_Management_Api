from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Task
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.http import HttpResponseForbidden
from django.views import View
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from django.contrib import messages


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        queryset = Task.objects.filter(created_by=self.request.user)

        # ---- FILTERS ----
        status = self.request.GET.get('status')
        priority = self.request.GET.get('priority')
        due_date = self.request.GET.get('due_date')

        if status:
            queryset = queryset.filter(status=status)

        if priority:
            queryset = queryset.filter(priority=priority)

        if due_date:
            queryset = queryset.filter(due_date__date=due_date)

        # ---- SORTING ----
        sort = self.request.GET.get('sort')

        if sort == 'due_date':
            queryset = queryset.order_by('due_date')

        elif sort == 'priority':
            # Custom priority ordering: High → Medium → Low
            queryset = queryset.extra(
                select={
                    'priority_order': """
                    CASE
                        WHEN priority = 'High' THEN 1
                        WHEN priority = 'Medium' THEN 2
                        WHEN priority = 'Low' THEN 3
                        ELSE 4
                    END
                    """
                },
                order_by=['priority_order']
            )

        return queryset
    
    # def get_queryset(self):
    #     # Only show tasks created by the logged-in user
    #     return Task.objects.filter(created_by=self.request.user)

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()  # Get the object first
        if obj.created_by != request.user:  # Check if the user owns the task
            return custom_permission_denied_view(request,"You do not have permission to view this task")
    
        return super().dispatch(request, *args, **kwargs)

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'tasks/task_form.html'
    fields = ['title', 'description', 'due_date', 'priority', 'status']
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user  # Set the user who created the task
        return super().form_valid(form)

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = 'tasks/task_form.html'
    fields = ['title', 'description', 'due_date', 'priority', 'status']

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()  # Get the object first
        if obj.created_by != request.user:  # Check if the user owns the task
            return custom_permission_denied_view(request,"You do not have permission to update this task")
        
        if obj.status == 'Completed':
            messages.error(request, "Completed tasks cannot be edited.")
            return redirect('task_detail', pk=obj.pk)
    
        return super().dispatch(request, *args, **kwargs)
        
    def form_valid(self, form):
        task = self.get_object()
        # Check if the status changes to 'Completed'

        if 'status' in form.changed_data:
            if form.cleaned_data['status'] == 'Completed':
                form.instance.mark_as_completed()
            elif form.cleaned_data['status'] == 'Pending':
                form.instance.mark_as_pending()

        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('task_detail', kwargs={'pk': self.object.pk})

class TaskStatusUpdateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk, created_by=request.user)

        # Toggle completion status
        if task.status == 'Completed':
            task.status = 'Pending'
            task.completed_at = None  # Reset the completed timestamp
        else:
            task.status = 'Completed'
            task.completed_at = timezone.now()  # Set the completed timestamp

        task.save()
        return JsonResponse({'status': task.status, 'id': task.pk})
      
class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('task_list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()  # Get the object first
        if obj.created_by != request.user:  # Check if the user owns the task
            return custom_permission_denied_view(request,"You do not have permission to Delete this task")

        return super().dispatch(request, *args, **kwargs)
    
    ###USER AUTHENTICATION###
from django.contrib.auth import logout

def logout_view(request):
    # Assuming you have set up logout logic
    logout(request)
    return render(request, 'registration/logout.html')


###HANDLE PERMISSION VIEW####
def custom_permission_denied_view(request, message):
    messages.error(request, message)
    return render(request, 'tasks/permission_denied.html')



#####API SECTION####
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def mark_complete(self, request, pk=None):
        task = get_object_or_404(Task, pk=pk, created_by=request.user)
        task.mark_as_completed()  # Call your method to mark as completed
        serializer = self.get_serializer(task)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def mark_pending(self, request, pk=None):
        task = get_object_or_404(Task, pk=pk, created_by=request.user)
        task.mark_as_pending()  # Call your method to mark as pending
        serializer = self.get_serializer(task)
        return Response(serializer.data)
    


### View to test Email ###
from django.core.management import call_command
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def send_due_task_notifications_view(request):
    # Call your management command
    call_command('send_due_task_notifications')
    return HttpResponse("Task due-soon notifications sent successfully!")