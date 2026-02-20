from django.contrib import admin
from . import models


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "owner",
    )


@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "project_id",
        "status",
        "priority",
        "deadline",
    )
