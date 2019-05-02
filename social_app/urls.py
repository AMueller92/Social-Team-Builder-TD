from django.urls import path

from . import views

app_name = 'social_app'
urlpatterns = [
    path('', views.ProjectListView.as_view(), name='home'),
    path('project/<pk>', views.ProjectDetailView.as_view(), name='project-detail'),
    path('profile/<pk>', views.ProfileDetailView.as_view(), name='profile'),
]