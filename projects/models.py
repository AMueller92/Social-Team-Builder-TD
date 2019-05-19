from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Timestampable(models.Model):
    ''' 
        Abstract Model to give Models where it's used on extra
        Functionality.
    '''
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
    '''Project Model'''
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='projects')
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=600)
    duration = models.IntegerField()
    requirements = models.CharField(max_length=255)

    @property
    def available_positions(self):
        '''Model property extracting Positions which are available'''
        return self.positions.exclude(applications__status='A')

    def __str__(self):
        return self.title


class Position(models.Model):
    '''Position Model'''
    project = models.ForeignKey(Project,
                                on_delete=models.CASCADE,
                                related_name='positions')
    name = models.CharField(max_length=100)
    skills = models.ManyToManyField('accounts.Skill', blank=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    description = models.CharField(max_length=500)
    length = models.IntegerField()

    def __str__(self):
        return self.name


class Application(Timestampable, models.Model):
    '''Model to handle User Applications for a Position'''
    STATUS_CHOICES = (
        ('P', 'Pending'),
        ('A', 'Accepted'),
        ('R', 'Rejected'),
    )
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    position = models.ForeignKey(Position,
                                 on_delete=models.CASCADE,
                                 related_name='applications')
    status = models.CharField(max_length=1,
                              choices=STATUS_CHOICES,
                              default='P')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Applicant: {self.applicant}"