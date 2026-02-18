from django.db import models
from datetime import date
from django.core.exceptions import ValidationError
from django.conf import settings


class Project(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="projects")

    def __str__(self):
        return self.name


class TaskStatus(models.TextChoices):
    TODO = "todo", "To do"
    IN_PROGRESS = "in_progress", "In progress"
    DONE = "done", "Done"


class TaskPriority(models.IntegerChoices):
    LOW = 1, "Low"
    MEDIUM = 2, "Medium"
    HIGH = 3, "High"


class Task(models.Model):
    name = models.CharField(max_length=255)

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="tasks",
    )

    status = models.CharField(
        max_length=20,
        choices=TaskStatus.choices,
        default=TaskStatus.TODO,
    )

    priority = models.IntegerField(
        choices=TaskPriority.choices,
        default=TaskPriority.MEDIUM,
    )

    deadline = models.DateField(
        null=True,
        blank=True,
        help_text="Optional deadline for the task",
    )

    def toggle_status(self):
        if self.status == TaskStatus.DONE:
            self.status = TaskStatus.TODO
        else:
            self.status = TaskStatus.DONE
        self.save()

    def clean(self):
        super().clean()
        if self.deadline and self.deadline < date.today():
            raise ValidationError("Deadline cannot be in the past")

    def __str__(self):
        return self.name
