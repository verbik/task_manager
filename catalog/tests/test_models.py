from django.contrib.auth import get_user_model
from django.test import TestCase

from catalog.models import Position, Task, TaskType


class PositionModelTest(TestCase):

    def test_str(self):
        position = Position.objects.create(name="test_position")
        self.assertEqual(position.name, str(position))


class TaskTypeModelTest(TestCase):
    def test_str(self):
        task_type = TaskType(
            name="test_task_type"
        )
        self.assertEqual(task_type.name, str(task_type))


class EmployeeModelTest(TestCase):
    def setUp(self) -> None:
        self.position = Position.objects.create(name="test_position")

    def test_create_employee(self):
        username = "test_employee"
        password = "abcde123"
        employee = get_user_model().objects.create_user(
            username=username,
            password=password,
            position=self.position
        )
        self.assertEqual(employee.username, username)
        self.assertEqual(employee.position, self.position)
        self.assertTrue(employee.check_password(password))

    def test_str(self):
        employee = get_user_model().objects.create_user(
            username="test_username",
            password="test123password",
            position=self.position
        )
        self.assertEqual(str(employee),
                         (f"{employee.username}: "
                          f"{employee.first_name} {employee.last_name} "
                          f"({employee.position})"))


class TaskModelTest(TestCase):
    def setUp(self) -> None:
        self.task_type = TaskType.objects.create(name="type")

    def test_str(self):
        task = Task.objects.create(name="task",
                                   task_type=self.task_type,
                                   description="test description",
                                   deadline="2022-12-11",
                                   priority="low")
        self.assertEqual(task.name, str(task))
