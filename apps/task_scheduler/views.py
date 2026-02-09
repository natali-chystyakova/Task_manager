from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, Task
from .forms import ProjectForm, TaskForm


# Список проектов
def project_list(request):
    projects = Project.objects.all()
    return render(request, "task_scheduler/project_list.html", {"task_scheduler": projects})


# Создание проекта
def project_create(request):
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("project_list")

    return render(request, "task_scheduler/project_form.html", {"form": form})


# Обновление проекта
def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk)
    form = ProjectForm(request.POST or None, instance=project)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("project_list")

    return render(request, "task_scheduler/project_form.html", {"form": form})


# Удаление проекта
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.method == "POST":
        project.delete()
        return redirect("project_list")

    return render(request, "task_scheduler/project_confirm_delete.html", {"project": project})


# Список задач проекта
def task_list(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    tasks = project.tasks.all()

    return render(
        request,
        "tasks/task_list.html",
        {
            "project": project,
            "tasks": tasks,
        },
    )


# #Создание задачи в проекте
# def task_create(request, project_id):
#     project = get_object_or_404(Project, id=project_id)
#     form = TaskForm(request.POST or None)
#
#     if request.method == "POST" and form.is_valid():
#         task = form.save(commit=False)
#         task.project = project
#         task.save()
#         return redirect("task_list", project_id=project.id)
#
#     return render(
#         request,
#         "tasks/task_form.html",
#         {
#             "form": form,
#             "project": project,
#         },
#     )


def task_create(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    form = TaskForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        task = form.save(commit=False)
        task.project = project
        task.save()

        # 🔥 HTMX: вернуть только строку задачи
        if request.headers.get("HX-Request"):
            return render(
                request,
                "tasks/partials/task_item.html",
                {"task": task},
            )

        # обычный fallback
        return redirect("task_list", project_id=project.id)

    return render(
        request,
        "tasks/task_form.html",
        {"form": form, "project": project},
    )


# Обновление задачи
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    form = TaskForm(request.POST or None, instance=task)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("task_list", project_id=task.project.id)

    return render(request, "tasks/task_form.html", {"form": form})


# Удаление задачи
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == "POST":
        project_id = task.project.id
        task.delete()
        return redirect("task_list", project_id=project_id)

    return render(request, "tasks/task_confirm_delete.html", {"task": task})


# Отметить задачу как выполненную
def task_mark_done(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.mark_done()

    if request.htmx:
        return render(request, "tasks/_task_row.html", {"task": task})

    return redirect("task_list", project_id=task.project.id)
