from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from tasks import views  # Change `your_app` to your actual app name
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)


urlpatterns = [
    path('tasks/', views.TaskListView.as_view(), name='task_list'),
    path('task/create/', views.TaskCreateView.as_view(), name='task_create'),
    path('task/<int:pk>/', views.TaskDetailView.as_view(), name='task_detail'),
    path('task/<int:pk>/update/', views.TaskUpdateView.as_view(), name='task_update'),
    path('task/<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('task/<int:pk>/status/', views.TaskStatusUpdateView.as_view(), name='task_status_update'),
    path('permission-denied/', views.custom_permission_denied_view, name='permission_denied'),
    path('api/', include(router.urls)),
]