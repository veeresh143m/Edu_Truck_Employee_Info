from django.db.models import Count
from rest_framework.viewsets import ModelViewSet

from .models import Department, Employee
from .serializers import DepartmentSerializer, EmployeeSerializer


class EmployeeViewSet(ModelViewSet):
    queryset = Employee.objects.select_related("department").all()
    serializer_class = EmployeeSerializer
    search_fields = ["first_name", "last_name", "email", "job_title", "department__name"]
    ordering_fields = ["first_name", "last_name", "hire_date", "created_at"]


class DepartmentViewSet(ModelViewSet):
    queryset = Department.objects.annotate(employee_count=Count("employees"))
    serializer_class = DepartmentSerializer
    search_fields = ["name"]
    ordering_fields = ["name", "created_at"]