from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from rest_framework import routers
from . import api_views

router = routers.DefaultRouter()
router.register(r'api/employees', api_views.EmployeeViewSet, basename='employee')
router.register(r'api/forms', api_views.DynamicFormViewSet, basename='form')
router.register(r'api/form-fields', api_views.FormFieldViewSet, basename='formfield')

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('employee_dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('profile/', views.employee_profile, name='employee_profile'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += router.urls