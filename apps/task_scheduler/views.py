from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, Task
from .forms import ProjectForm, TaskForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import render_to_string


@login_required
def project_list(request):
    projects = Project.objects.filter(owner=request.user).prefetch_related("tasks")

    if request.method == "POST":
        form = TaskForm(request.POST)
        project_id = request.POST.get("project_id")
        project = get_object_or_404(Project, id=project_id)

        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()

            if request.headers.get("HX-Request"):
                return render(
                    request,
                    "task_scheduler/partials/task_item.html",
                    {"task": task},
                )

            return redirect("task_scheduler:project_list")
    else:
        form = TaskForm()

    return render(request, "task_scheduler/project_list.html", {"task_scheduler": projects, "form": form})


def project_create(request):
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            # 2. Назначаем владельца из паспорта запроса 👤
            project.owner = request.user

            # 3. Теперь сохраняем по-настоящему
            project.save()

            if request.headers.get("HX-Request"):
                # 1. Рендерим новый проект
                project_html = render_to_string(
                    "task_scheduler/partials_pro/project_item.html", {"project": project}, request=request
                )
                # 2. Рендерим кнопку "Add Project" (OOB), чтобы она заменила форму
                button_html = render_to_string("task_scheduler/partials_pro/add_project_button.html", request=request)
                # Оборачиваем кнопку в OOB-контейнер
                oob_button = f'<div id="project-form-container" hx-swap-oob="true">{button_html}</div>'

                return HttpResponse(project_html + oob_button)

            return redirect("task_scheduler:project_list")

        # Если форма НЕВАЛИДНА (ошибки) при POST запросе
        if request.headers.get("HX-Request"):
            return render(request, "task_scheduler/partials_pro/project_form_inner.html", {"form": form})

    else:
        # GET запрос: создаем пустую форму
        form = ProjectForm()

    # Ответ для GET запроса (или обычного, или HTMX открытия формы)
    if request.headers.get("HX-Request"):
        return render(request, "task_scheduler/partials_pro/project_form_inner.html", {"form": form})

    return render(request, "task_scheduler/project_form.html", {"form": form})


@login_required
def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    form = ProjectForm(request.POST or None, instance=project)

    if request.method == "POST" and form.is_valid():
        form.save()
        if request.headers.get("HX-Request"):
            # возвращаем обновлённую карточку проекта
            return render(request, "task_scheduler/partials_pro/project_item.html", {"project": project})
        return redirect("task_scheduler:project_list")

    if request.headers.get("HX-Request"):
        return render(request, "task_scheduler/partials_pro/project_edit_form.html", {"form": form, "project": project})

    return render(request, "task_scheduler/project_form.html", {"form": form})


@login_required
def project_delete(request, pk):
    # Ищем проект ТОЛЬКО среди тех, где owner = request.user 👤
    project = get_object_or_404(Project, pk=pk, owner=request.user)

    if request.method == "POST":
        project.delete()

        if request.headers.get("HX-Request"):
            return HttpResponse("")

        return redirect("task_scheduler:project_list")

    if request.headers.get("HX-Request"):
        return render(request, "task_scheduler/partials_pro/project_confirm_delete.html", {"project": project})

    return render(request, "task_scheduler/project_confirm_delete.html", {"project": project})


def task_create(request, project_id):
    project = get_object_or_404(Project, id=project_id, owner=request.user)

    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()

            if request.headers.get("HX-Request"):
                # Рендерим саму задачу (пойдет в конец списка)
                task_html = render_to_string(
                    "task_scheduler/tasks/partials/task_item.html", {"task": task}, request=request
                )

                return HttpResponse(task_html)

        # Если форма невалидна, возвращаем её с ошибками обратно в тот же контейнер
        if request.headers.get("HX-Request"):
            return render(request, "task_scheduler/tasks/partials/task_form.html", {"form": form, "project": project})

    # Обработка GET: когда пользователь нажал на кнопку "+ Add Task"
    if request.method == "GET" and request.headers.get("HX-Request"):
        return render(request, "task_scheduler/tasks/partials/task_form.html", {"project": project, "form": TaskForm()})

    return redirect("task_scheduler:project_list")


def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    form = TaskForm(request.POST or None, instance=task)

    if request.method == "POST" and form.is_valid():
        form.save()

        # 🔥 если HTMX — вернуть обновлённый task_item
        if request.headers.get("HX-Request"):
            return render(
                request,
                "task_scheduler/tasks/partials/task_item.html",
                {"task": task},
            )

        return redirect("task_scheduler:project_list")

    # если GET через HTMX — вернуть форму как partial
    if request.headers.get("HX-Request"):
        return render(
            request,
            "task_scheduler/tasks/partials/task_edit_form.html",
            {"form": form, "task": task},
        )

    return render(
        request,
        "task_scheduler/tasks/task_form.html",
        {"form": form, "project": task.project},
    )


def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == "POST":
        task.delete()

        if request.headers.get("HX-Request"):
            return HttpResponse("")

        return redirect("task_scheduler:project_list")

    if request.headers.get("HX-Request"):
        return render(
            request,
            "task_scheduler/tasks/partials/task_confirm_delete_partial.html",
            {"task": task},
        )

    return render(
        request,
        "task_scheduler/tasks/task_confirm_delete.html",
        {"task": task},
    )


def task_toggle_status(request, pk):
    task = get_object_or_404(Task, pk=pk)

    # Используем метод модели
    task.toggle_status()

    if request.headers.get("HX-Request"):
        return render(request, "task_scheduler/tasks/partials/task_item.html", {"task": task})

    # Резервный вариант для обычных запросов
    return redirect("task_scheduler:project_list")


def task_detail_partial(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, "task_scheduler/tasks/partials/task_item.html", {"task": task})


def project_detail_partial(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(
        request, "task_scheduler/partials_pro/project_item.html", {"project": project}  # Путь к твоему кусочку проекта
    )


def render_add_button(request):
    """Возвращает фрагмент с кнопкой 'Add Project'"""
    return render(request, "task_scheduler/partials_pro/add_project_button.html")


def render_add_button_task(request):
    """Возвращает фрагмент с кнопкой 'Add Project'"""
    return render(request, "task_scheduler/tasks/partials/add_task_button.html")
