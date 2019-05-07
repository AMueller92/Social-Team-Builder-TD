from django.urls import path

from . import views

app_name = 'accounts'
urlpatterns = [
    path('profile/<pk>', views.ProfileDetailView.as_view(), name='profile'),
]