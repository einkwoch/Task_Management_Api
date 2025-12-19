from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from tasks.models import Task

class Command(BaseCommand):
    help = 'Send email reminders for tasks due soon'

    def handle(self, *args, **kwargs):
        due_soon_tasks = Task.objects.filter(
            status='Pending',
            due_date__gte=timezone.now(),
            due_date__lte=timezone.now() + timedelta(hours=24),
        )

        for task in due_soon_tasks:
            if task.created_by.email:
                send_mail(
                    subject='⏰ Task Due Soon',
                    message=(
                        f'Hello {task.created_by.username},\n\n'
                        f'Your task "{task.title}" is due on {task.due_date}.\n\n'
                        'Please take action.'
                    ),
                    from_email=None,
                    recipient_list=[task.created_by.email],
                )

        self.stdout.write(
            self.style.SUCCESS('Task due-soon notifications sent successfully')
        )
