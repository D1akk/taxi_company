from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', index, name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('register-admin/', RegisterAdminView.as_view(), name='register-admin'),
    path('register-driver/', RegisterDriverView.as_view(), name='register-driver'),
    
    path('task-list', TaskListView.as_view(), name='tasks'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task'),
    path('task-create/', TaskCreateView.as_view(), name='task-create'),
    path('task-update/<int:pk>/', TaskUpdateView.as_view(), name='task-update'),
    path('task-delete/<int:pk>/', TaskDeleteView.as_view(), name='task-delete'),

    path('driver-list/', DriverListView.as_view(), name='driver-list'),
    path('driver/<int:pk>', DriverDetailView.as_view(), name='driver'),

    path('car-list/', CarListView.as_view(), name='car-list'),
    path('task/<int:pk>/export', generate_waybill, name='generate_waybill')
]
