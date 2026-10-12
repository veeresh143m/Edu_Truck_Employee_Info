from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.db.models.deletion import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render

from .forms import DepartmentForm, EmployeeForm, RegistrationForm
from .models import Department, Employee


def register(request):
    form = RegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        auth_login(request, user)
        messages.success(request, f"Welcome, {user.username}. Your account is ready.")
        return redirect("dashboard")
    return render(request, "employees/register.html", {"form": form})


@login_required
def dashboard(request):
    context = {
        "employee_count": Employee.objects.count(),
        "active_count": Employee.objects.filter(status=Employee.Status.ACTIVE).count(),
        "department_count": Department.objects.count(),
        "recent_employees": Employee.objects.select_related("department").order_by("-created_at")[:6],
    }
    return render(request, "employees/dashboard.html", context)


@login_required
def employee_list(request):
    employees = Employee.objects.select_related("department")
    query = request.GET.get("q", "").strip()
    department_id = request.GET.get("department", "")
    status = request.GET.get("status", "")
    if query:
        employees = employees.filter(
            Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(email__icontains=query)
            | Q(job_title__icontains=query)
        )
    if department_id:
        employees = employees.filter(department_id=department_id)
    if status:
        employees = employees.filter(status=status)
    return render(
        request,
        "employees/employee_list.html",
        {
            "employees": employees,
            "departments": Department.objects.all(),
            "statuses": Employee.Status.choices,
            "query": query,
            "selected_department": department_id,
            "selected_status": status,
        },
    )


@login_required
def employee_detail(request, pk):
    employee = get_object_or_404(Employee.objects.select_related("department"), pk=pk)
    return render(request, "employees/employee_detail.html", {"employee": employee})


@login_required
def employee_create(request):
    form = EmployeeForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        employee = form.save()
        messages.success(request, f"{employee} was added.")
        return redirect("employee_detail", pk=employee.pk)
    return render(request, "employees/employee_form.html", {"form": form, "title": "Add employee"})


@login_required
def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    form = EmployeeForm(request.POST or None, instance=employee)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, f"{employee} was updated.")
        return redirect("employee_detail", pk=employee.pk)
    return render(request, "employees/employee_form.html", {"form": form, "title": "Edit employee", "employee": employee})


@login_required
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == "POST":
        name = str(employee)
        employee.delete()
        messages.success(request, f"{name} was deleted.")
        return redirect("employee_list")
    return render(request, "employees/confirm_delete.html", {"employee": employee, "object_type": "employee"})


@login_required
def department_list(request):
    departments = Department.objects.annotate(employee_count=Count("employees"))
    return render(request, "employees/department_list.html", {"departments": departments})


@login_required
def department_create(request):
    form = DepartmentForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Department was added.")
        return redirect("department_list")
    return render(request, "employees/department_form.html", {"form": form, "title": "Add department"})


@login_required
def department_update(request, pk):
    department = get_object_or_404(Department, pk=pk)
    form = DepartmentForm(request.POST or None, instance=department)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Department was updated.")
        return redirect("department_list")
    return render(request, "employees/department_form.html", {"form": form, "title": "Edit department"})

@login_required
def department_delete(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == "POST":
        try:
            department.delete()
        except ProtectedError:
            messages.error(request, "This department still has employees assigned. Reassign them before deleting it.")
        else:
            messages.success(request, "Department was deleted.")
        return redirect("department_list")
    return render(request, "employees/confirm_delete.html", {"department": department, "object_type": "department"})