from django.contrib import admin
from .models import CustomUser, Task

class Task_Ad(admin.ModelAdmin):
    list_display = ('title',
                    'due_date',
                    'priority',
                    'status',
                    'created_by',
                    'completed_at',
                    'created_at',
                    'updated_at')

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Task,Task_Ad)