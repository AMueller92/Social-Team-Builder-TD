from django.urls import path

from . import views

app_name = 'projects'
urlpatterns = [
    path('search/', views.search, name='search'),
    path('new/', views.NewProjectView.as_view(), name='new_project'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('applications/', views.applications_view, name='applications'),
    path('delete/<pk>/', views.DeleteProjectView.as_view(), name='delete_project'),
    path('<pk>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('edit/<pk>', views.EditProjectView.as_view(), name='edit_project'),
    path('position/<position_pk>/application', views.position_apply, name='apply'),
    path('applications/<application_pk>/<status>', views.application_status_view, name='app_status')
]