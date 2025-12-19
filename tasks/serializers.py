from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 
                  'priority', 'status', 'created_by', 
                  'completed_at', 'created_at', 'updated_at']
        read_only_fields = ['created_by', 'completed_at',
                            'created_at', 'updated_at']  # Ensure these fields cannot be set by the user