from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from catalog.models import Position


class AdminSiteTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="testadmin"
        )
        self.client.force_login(self.admin_user)
        position = Position.objects.create(name="position")
        self.employee = get_user_model().objects.create_user(
            username="employee",
            password="test_employee",
            position=position
        )

    def test_employee_position_listed(self):
        """
        Test that employee's position is in list_display
        on employee admin page
        """
        url = reverse("admin:catalog_employee_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.employee.position)
