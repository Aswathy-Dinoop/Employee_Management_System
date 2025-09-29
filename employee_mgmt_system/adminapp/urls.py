from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from . import api_views

urlpatterns = [
   
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('view_employees/', views.view_employees, name='view_employees'),
    path('edit/<int:pk>/', views.employee_edit, name='employee_edit'),
    path('delete/<int:pk>/', views.employee_delete, name='employee_delete'),


]
urlpatterns += [
    # API endpoints
    path('api/register/', api_views.RegisterView.as_view(), name='api_register'),
    path('create_employee/', views.employee_create, name='employee_create'),
    path('api/login/', api_views.CustomTokenObtainPairView.as_view(), name='api_login'),
    path('api/change-password/', api_views.ChangePasswordView.as_view(), name='api_change_password'),
    path('api/profile/', api_views.ProfileView.as_view(), name='api_profile'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)