from django.urls import path

from . import views

app_name = 'accounts'
urlpatterns = [
    path('profile/', views.user_profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/<pk>', views.any_user_profile, name='any_profile'),
]