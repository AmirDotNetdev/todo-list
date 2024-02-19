from django.urls import path
from . import views

urlpatterns = [
    path('', views.TaskList.as_view(), name = 'tasks'),
    path('task/<int:pk>/', views.TaskDetail.as_view(), name = 'task'),
    path('task-update/<int:pk>/', views.TaskUpdate.as_view(), name = 'update'),
    path('task-create/', views.TaskCreate.as_view(), name = 'create'),
    path('task-delete/<int:pk>/', views.TaskDelete.as_view(), name = 'delete'),
]
