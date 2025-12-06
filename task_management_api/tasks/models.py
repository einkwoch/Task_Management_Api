from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateTimeField()
    priority = models.CharField(choices=PRIORITY_CHOICES, max_length=10)
    status = models.CharField(choices=STATUS_CHOICES, default='Pending', max_length=10)
    created_by = models.ForeignKey(User, related_name='tasks', on_delete=models.CASCADE)
    completed_at = models.DateTimeField(null=True, blank=True)

    def clean(self):
        if self.due_date <= timezone.now():
            raise ValidationError("Due date must be in the future.")