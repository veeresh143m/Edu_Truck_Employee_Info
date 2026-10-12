from rest_framework.routers import DefaultRouter

from .api import DepartmentViewSet, EmployeeViewSet

router = DefaultRouter()
router.register("employees", EmployeeViewSet)
router.register("departments", DepartmentViewSet)

urlpatterns = router.urls