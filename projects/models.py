from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone


class Timestampable(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    @property
    def changed(self):
        return True if self.modified_at else False

    def save(self, *args, **kwargs):
        if self.pk:
            self.modified = timezone.now()
        return super(Timestampable, self).save(*args, **kwargs)


class Project(Timestampable, models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=600)
    duration = models.IntegerField()
    requirements = models.CharField(max_length=255)

    def __str__(self):
        return f"Project: {self.title}"


class Position(models.Model):
    name = models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    skills = models.ManyToManyField('accounts.Skill', blank=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    description = models.CharField(max_length=500)

    def __str__(self):
        return f"Position: {self.name}"


class Notification(Timestampable, models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return f"Notification: {self.title}"


class UserPositionApplication(models.Model):
    '''Ensures that a User can only apply to one Position'''
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['user', 'position']
