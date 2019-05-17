from django.contrib import admin

from .models import Project, Position, Application

admin.site.register(Project)
admin.site.register(Position)
admin.site.register(Application)
