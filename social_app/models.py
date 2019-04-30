from django.db import models
from django.contrib.auth import get_user_model

from .behaviors import Timestampable

class Profile(Timestampable, models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=50, default=user.username)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    description = models.CharField(max_length=600, blank=True, default="")
    skills = models.ManyToManyField(Skills, on_delete=models.PROTECT)

    def __str__(self):
        return f"Profile of {self.user}"


class Project(Timestampable, models.Model):
    user = models.ManyToOne(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=150, default="Please enter a project title")
    description = models.CharField(max_length=600, default="Please enter a project description")

    def __str__(self):
        return f"Project: {self.title}"


class Skills(models.Model):
    PYTHON = 'PY'
    JAVA = 'JV'
    JAVASCRIPT = 'JS'
    PHP = 'PHP'
    RUBY = 'RU'
    SKILL_CHOICES = (
        (PYTHON, 'Python'),
        (JAVA, 'Java'),
        (JAVASCRIPT, 'JavaScript'),
        (PHP, 'Php'),
        (RUBY, 'Ruby'),
    )
    name = models.CharField(max_length=50, choices=SKILL_CHOICES, default="")

    def __str__(self):
        return f"Skill: {self.name}"


class Positions(models.Model):
    name = models.CharField(max_length=100)
    project = models.ForeignKey(Project)
    skills = models.ManyToManyField(Skills, on_delete=models.PROTECT)
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)

    def __str__(self):
        return f"Position: {self.name}"


class Notifications(Timestampable, models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return f"Notification: {self.title}"


class UserPositionApplication(models.Model):
    '''Ensures that a User can only apply to one Position'''
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    position = models.ForeignKey(Positions, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['user', 'position']
