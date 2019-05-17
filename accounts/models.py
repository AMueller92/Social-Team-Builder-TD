from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
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


class Skill(models.Model):
    PYTHON = 'PY'
    JAVA = 'JV'
    JAVASCRIPT = 'JS'
    PHP = 'PHP'
    RUBY = 'RU'
    DESIGNER = 'DES'
    ANDROID = 'AN'
    WORDPRESS = 'WP'
    IOS = 'IOS'
    SKILL_CHOICES = (
        (PYTHON, 'Python'),
        (JAVA, 'Java'),
        (JAVASCRIPT, 'JavaScript'),
        (PHP, 'Php'),
        (RUBY, 'Ruby'),
        (DESIGNER, 'Designer'),
        (ANDROID, 'Android'),
        (WORDPRESS, 'WordPress'),
        (IOS, 'iOS'),
    )
    name = models.CharField(max_length=50, choices=SKILL_CHOICES, default="", blank=True)

    def __str__(self):
        return self.get_name_display()


class Profile(Timestampable, models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True, default='')
    last_name = models.CharField(max_length=50, blank=True, default='')
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    description = models.CharField(max_length=600, blank=True, default="")
    skills = models.ManyToManyField(Skill, blank=True)

    def __str__(self):
        return f"Profile of {self.user} PK: {self.pk}"


class SelfChoosenSkill(models.Model):
    name = models.CharField(max_length=40, blank=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='extra_skills')

    def __str__(self):
        return self.name


class UserProject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=90)
    url = models.URLField()

    def __str__(self):
        return self.title
