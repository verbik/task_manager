from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from catalog.models import (Task,
                            TaskType,
                            Position)
from catalog.forms import (TaskTypeSearchForm)


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
