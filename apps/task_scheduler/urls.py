from django.urls import path
from . import views

app_name = "task_scheduler"


urlpatterns = [
    path("", views.project_list, name="project_list"),
    path("task_scheduler/create/", views.project_create, name="project_create"),
    path("task_scheduler/<int:pk>/edit/", views.project_update, name="project_update"),
    path("task_scheduler/<int:pk>/delete/", views.project_delete, name="project_delete"),
    # path("task_scheduler/<int:project_id>/tasks/", views.task_list, name="task_list"),
    path("task_scheduler/<int:project_id>/tasks/create/", views.task_create, name="task_create"),
    path("tasks/<int:pk>/edit/", views.task_update, name="task_update"),
    path("tasks/<int:pk>/delete/", views.task_delete, name="task_delete"),
    path("tasks/<int:pk>/toggle/", views.task_toggle_status, name="task_toggle_status"),
    path("tasks/<int:pk>/detail/", views.task_detail_partial, name="task_detail_partial"),
    path("task_scheduler/<int:pk>/detail/", views.project_detail_partial, name="project_detail_partial"),
    path("task_scheduler/add-button/", views.render_add_button, name="render_add_button"),
]
