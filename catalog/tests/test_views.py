from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from catalog.models import TaskType, Task, Position

TASK_TYPE_LIST_URL = reverse("catalog:task-type-list")
TASK_LIST_URL = reverse("catalog:task-list")
EMPLOYEE_LIST_URL = reverse("catalog:employee-list")
HOME_URL = reverse("catalog:index")


class LoginRequiredViewsTest(TestCase):
    def test_home_page_login_required(self):
        res = self.client.get(HOME_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_employees_login_required(self):
        res = self.client.get(EMPLOYEE_LIST_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_task_login_required(self):
        res = self.client.get(TASK_LIST_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_task_type_login_required(self):
        res = self.client.get(TASK_TYPE_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class RetrieveListsTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_task_type_list(self):
        TaskType.objects.create(name="test1")
        TaskType.objects.create(name="test2")
        response = self.client.get(TASK_TYPE_LIST_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = TaskType.objects.all()
        self.assertEqual(
            list(response.context["task_types_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "catalog/task_types_list")

    def test_retrieve_task_list(self):
        task_type = TaskType.objects.create(name="test_name")
        Task.objects.create(name="test_task", task_type=task_type)
        Task.objects.create(name="test_task", task_type=task_type)
        response = self.client.get(TASK_LIST_URL)
        self.assertEqual(response.status_code, 200)
        tasks = Task.objects.all()
        self.assertEqual(
            list(response.context["task_list"]),
            list(tasks)
        )
        self.assertTemplateUsed(response, "catalog/task_list.html")


class SearchTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="12345"
        )
        self.client.force_login(self.user)

    def test_task_type_search(self):
        m1 = TaskType.objects.create(name="abc")
        m2 = TaskType.objects.create(name="ab")
        TaskType.objects.create(name="bc")
        response = self.client.get(reverse("catalog:task-type-list"),
                                   args={"name": "ab"})
        response_task_type_list = list(
            response.context["task_types_list"]).sort(key=lambda m: m.id)
        expected_task_type_list = [m1, m2].sort(key=lambda m: m.id)

        self.assertEqual(expected_task_type_list,
                         response_task_type_list)

    def test_Task_search(self):
        m1 = TaskType.objects.create(name="abc")
        task1 = Task.objects.create(name="ab", task_type=m1)
        task2 = Task.objects.create(name="abc", task_type=m1)
        Task.objects.create(name="bc", task_type=m1)
        response = self.client.get(reverse("catalog:task-list"),
                                   args={"name": "ab"})
        response_task_list = list(
            response.context["task_list"]).sort(key=lambda m: m.id)
        expected_task_list = [task1, task2].sort(key=lambda m: m.id)

        self.assertEqual(expected_task_list,
                         response_task_list)

    def test_driver_search(self):
        position = Position.objects.create(name="test")
        employee1 = get_user_model().objects.create_user(
            username="abc",
            password="test1234",
            position=position
        )
        employee2 = get_user_model().objects.create_user(
            username="ab",
            password="test123445",
            position=position
        )
        response = self.client.get(reverse("catalog:employee-list"),
                                   args={"username": "ab"})
        response_employee_list = list(
            response.context["employee_list"]).sort(key=lambda m: m.id)
        expected_employee_list = [employee1, employee2].sort(key=lambda m: m.id)

        self.assertEqual(expected_employee_list,
                         response_employee_list)


class ToggleAssignToTaskViewTest(TestCase):
    def setUp(self) -> None:
        user = self.user = get_user_model().objects.create_user(
            username="user",
            password="test"
        )
        self.client.force_login(user)
        self.task_type = TaskType.objects.create(
            name="test",
        )
        self.task = Task.objects.create(
            name="test",
            task_type=self.task_type
        )

    def test_toggle_assign_to_task(self):
        url = reverse("catalog:toggle-task-assign", args=[self.task.id])
        self.client.get(url)
        self.assertIn(self.user, self.task.assignees.all())

        self.client.get(url)
        self.assertNotIn(self.user, self.task.assignees.all())
