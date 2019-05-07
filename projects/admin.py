from django.contrib import admin

from .models import Project, Position, Notification, UserPositionApplication

admin.site.register(Project)
admin.site.register(Position)
admin.site.register(Notification)
admin.site.register(UserPositionApplication)
