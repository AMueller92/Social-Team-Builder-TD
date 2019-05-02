from django.contrib import admin

from .models import (Skills, Profile, Project, Positions,
                     Notifications, UserPositionApplication)

admin.site.register(Skills)
admin.site.register(Profile)
admin.site.register(Project)
admin.site.register(Positions)
admin.site.register(Notifications)
admin.site.register(UserPositionApplication)
