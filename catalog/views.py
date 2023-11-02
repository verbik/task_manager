from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from catalog.models import (Task,
                            TaskType,
                            Position,
                            Employee)
from catalog.forms import (TaskTypeSearchForm,
                           TaskSearchForm,
                           EmployeeSearchForm,
                           EmployeeCreationForm,
                           EmployeePositionUpdateForm,
                           PositionSearchForm)


@login_required
def index(request):
    """View function for the home page of the site"""

    num_tasks = Task.objects.count()
    num_types_tasks = TaskType.objects.count()
    num_position = Position.objects.count()
    num_employee = get_user_model().objects.count()

    context = {
        "num_tasks": num_tasks,
        "num_types_tasks": num_types_tasks,
        "num_position": num_position,
        "num_employee": num_employee
    }

    return render(request,
                  "catalog/index.html",
                  context=context)


# Task Type Views
class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    context_object_name = "task_types_list"
    template_name = "catalog/task_types_list"
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskTypeListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TaskTypeSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        queryset = TaskType.objects.all()
        name = self.request.GET.get("name")

        if name:
            return queryset.filter(name__icontains=name)

        return queryset


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    fields = "__all__"
    template_name = "catalog/task_type_form.html"
    success_url = reverse_lazy("catalog:task-type-list")


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    fields = "__all__"
    template_name = "catalog/task_type_form.html"
    success_url = reverse_lazy("catalog:task-type-list")


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    template_name = "catalog/task_type_confirm_delete.html"
    success_url = reverse_lazy("catalog:task-type-list")


# Task Views
class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        task_type = self.request.GET.get("task_type", "")
        unique_task_types = TaskType.objects.values_list("name",
                                                         flat=True).distinct()
        context["unique_task_types"] = unique_task_types

        context["search_form"] = TaskSearchForm(
            initial={
                "name": name,
                "task_type": task_type
            }
        )

        return context

    def get_queryset(self):
        queryset = Task.objects.all().select_related("task_type")
        name = self.request.GET.get("name")
        task_type = self.request.GET.get("task_type")

        if name:
            queryset = queryset.filter(name__icontains=name)

        if task_type:
            queryset = queryset.filter(task_type=task_type)

        return queryset


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy("catalog:task-list")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy("catalog:task-list")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("catalog:task-list")


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task


@login_required
def toggle_assign_to_task(request, pk):
    employee = get_user_model().objects.get(id=request.user.id)
    if (
        Task.objects.get(id=pk) in employee.tasks.all()
    ):  # probably could check if car exists
        employee.tasks.remove(pk)
    else:
        employee.tasks.add(pk)
    return HttpResponseRedirect(reverse_lazy("catalog:task-detail", args=[pk]))


# Employee Views
class EmployeeListView(LoginRequiredMixin, generic.ListView):
    model = Employee
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(EmployeeListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = EmployeeSearchForm(
            initial={"username": username}
        )
        return context

    def get_queryset(self):
        queryset = super(EmployeeListView, self).get_queryset()
        username = self.request.GET.get("username")

        if username:
            return queryset.filter(username__icontains=username)

        return queryset


class EmployeeCreateView(LoginRequiredMixin, generic.CreateView):
    model = Employee
    form_class = EmployeeCreationForm


class EmployeeDetailView(LoginRequiredMixin, generic.DetailView):
    model = Employee
    queryset = Employee.objects.all().prefetch_related("tasks__task_type")


class EmployeeUpdatePositionView(LoginRequiredMixin, generic.UpdateView):
    model = Employee
    form_class = EmployeePositionUpdateForm
    success_url = reverse_lazy("catalog:employee-list")


class EmployeeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Employee
    success_url = reverse_lazy("catalog:employee-list")


# Position Views
class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PositionListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = PositionSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        queryset = Position.objects.all()
        name = self.request.GET.get("name")

        if name:
            return queryset.filter(name__icontains=name)

        return queryset


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("catalog:position-list")


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("catalog:position-list")


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Position
    success_url = reverse_lazy("catalog:position-list")
