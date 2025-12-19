from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth import get_user_model

###CUSTOM USER MODEL####
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not username:
            raise ValueError('The Username field must be set')
        
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, password, **extra_fields)

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)

    # Use the custom user manager
    objects = CustomUserManager()

    def __str__(self):
        return self.username
    



###TASK MANAGEMENT MODEL###

### Import Custom User ###

User = get_user_model()

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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.due_date <= timezone.now():
            raise ValidationError("Due date must be in the future.")
        
    def mark_as_completed(self):
        self.status = 'Completed'
        self.completed_at = timezone.now()  # Set the completed_at timestamp
        self.save()

    def mark_as_pending(self):
        self.status = 'Pending'
        self.completed_at = None  # Reset timestamp
        self.save()