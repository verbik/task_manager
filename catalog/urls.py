from django.urls import path

from .views import (
    index,
    TaskTypeListView,
    TaskTypeCreateView,
    TaskTypeUpdateView,
    TaskTypeDeleteView,
    TaskListView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    TaskDetailView,
    toggle_assign_to_task,
    EmployeeListView,
    EmployeeDetailView,
    EmployeeCreateView,
    EmployeeUpdatePositionView,
    EmployeeDeleteView
)

urlpatterns = [
    path("", index, name="index"),
    path(
        "task-types/",
        TaskTypeListView.as_view(),
        name="task-type-list"
    ),
    path(
        "task-types/create/",
        TaskTypeCreateView.as_view(),
        name="task-type-create"
    ),
    path(
        "task-types/<int:pk>/update/",
        TaskTypeUpdateView.as_view(),
        name="task-type-update"
    ),
    path(
        "task-types/<int:pk>/delete/",
        TaskTypeDeleteView.as_view(),
        name="task-type-delete"
    ),
    # Task
    path(
        "tasks/",
        TaskListView.as_view(),
        name="task-list"
    ),
    path(
        "tasks/create/",
        TaskCreateView.as_view(),
        name="task-create"
    ),
    path(
        "tasks/<int:pk>/update/",
        TaskUpdateView.as_view(),
        name="task-update"
    ),
    path(
        "tasks/<int:pk>/delete/",
        TaskDeleteView.as_view(),
        name="task-delete"
    ),
    path(
        "tasks/<int:pk>/",
        TaskDetailView.as_view(),
        name="task-detail"
    ),
    path(
        "tasks/<int:pk>/toggle-assign/",
        toggle_assign_to_task,
        name="toggle-task-assign"
    ),
    # Employee
    path(
        "employees/",
        EmployeeListView.as_view(),
        name="employee-list"
    ),
    path(
        "employees/<int:pk>/",
        EmployeeDetailView.as_view(),
        name="employee-detail"
    ),
    path(
        "employees/create/",
        EmployeeCreateView.as_view(),
        name="employee-create"
    ),
    path(
        "employees/<int:pk>/update/",
        EmployeeUpdatePositionView.as_view(),
        name="employee-update"
    ),
    path(
        "employee/<int:pk>/delete/",
        EmployeeDeleteView.as_view(),
        name="employee-delete"
    )
]

app_name = "catalog"
