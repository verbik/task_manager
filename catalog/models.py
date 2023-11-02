from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class Position(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Employee(AbstractUser):
    position = models.ForeignKey(Position,
                                 related_name="employees",
                                 null=True,
                                 on_delete=models.CASCADE)

    class Meta:
        verbose_name = "employee"
        verbose_name_plural = "employees"

    def __str__(self):
        return (f"{self.username}: "
                f"{self.first_name} {self.last_name} "
                f"({self.position})")

    def get_absolute_url(self):
        return reverse("catalog:employee-detail", kwargs={"pk": self.pk})


class TaskType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Task(models.Model):
    PRIORITY_CHOICES = [
        ("urgent", "🔴 Urgent!!! 🔴"),
        ("high", "🟠 High priority! 🟠"),
        ("medium", "🟡 Medium priority. 🟡"),
        ("low", "🟢 Low priority. 🟢")
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(null=True,
                                   blank=True)
    deadline = models.DateTimeField(null=True,
                                    blank=True)
    is_completer = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=50,
        choices=PRIORITY_CHOICES,
        null=True,
    )
    task_type = models.ForeignKey(TaskType,
                                  related_name="tasks",
                                  on_delete=models.CASCADE)
    assignees = models.ManyToManyField(Employee,
                                       related_name="tasks")

    def __str__(self):
        return self.name
