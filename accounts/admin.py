from django.contrib import admin

from .models import Skill, Profile, SelfChoosenSkill, UserProject

admin.site.register(Skill)
admin.site.register(Profile)
admin.site.register(SelfChoosenSkill)
admin.site.register(UserProject)
