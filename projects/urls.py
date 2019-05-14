from django.urls import path

from . import views

app_name = 'projects'
urlpatterns = [
    path('new/', views.NewProjectView.as_view(), name='new_project'),
    path('delete/<pk>/', views.DeleteProjectView.as_view(), name='delete_project'),
    path('<pk>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('edit/<pk>', views.EditProjectView.as_view(), name='edit_project'),
]