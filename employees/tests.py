from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from .models import Department, Employee


class EmployeeManagementTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="hr", password="a-strong-test-password")
        self.department = Department.objects.create(name="People")
        self.employee = Employee.objects.create(
            first_name="Avery",
            last_name="Morgan",
            email="avery@example.com",
            job_title="Coordinator",
            department=self.department,
            hire_date="2024-01-15",
        )

    def test_employee_pages_require_login(self):
        response = self.client.get(reverse("employee_list"))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('employee_list')}")

    def test_registration_signs_in_and_opens_dashboard(self):
        response = self.client.post(reverse("register"), {
            "username": "new-hr-user",
            "password1": "abc",
            "password2": "abc",
        })
        self.assertRedirects(response, reverse("dashboard"), fetch_redirect_response=False)
        new_user = get_user_model().objects.get(username="new-hr-user")
        self.assertTrue(new_user.is_active)
        self.assertEqual(self.client.get(reverse("dashboard")).status_code, 200)

    def test_employee_can_be_updated_and_deleted(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("employee_update", args=[self.employee.pk]), {
            "first_name": "Avery",
            "last_name": "Morgan",
            "email": "avery@example.com",
            "job_title": "Senior Coordinator",
            "department": self.department.pk,
            "hire_date": "2024-01-15",
            "status": Employee.Status.ACTIVE,
        })
        self.assertRedirects(response, reverse("employee_detail", args=[self.employee.pk]))
        self.employee.refresh_from_db()
        self.assertEqual(self.employee.job_title, "Senior Coordinator")
        self.client.post(reverse("employee_delete", args=[self.employee.pk]))
        self.assertFalse(Employee.objects.filter(pk=self.employee.pk).exists())

    def test_employee_api_requires_authentication_and_supports_crud(self):
        client = APIClient()
        endpoint = "/api/employees/"
        self.assertEqual(client.get(endpoint).status_code, 403)
        client.force_authenticate(self.user)
        self.assertEqual(client.get(endpoint).status_code, 200)
        response = client.post(endpoint, {
            "first_name": "Taylor",
            "last_name": "Reed",
            "email": "taylor@example.com",
            "job_title": "Analyst",
            "department": self.department.pk,
            "hire_date": "2025-03-01",
            "status": "active",
        }, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Employee.objects.filter(email="taylor@example.com").exists())