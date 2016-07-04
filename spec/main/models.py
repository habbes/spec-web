from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Skill(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(default='')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    skills = models.ManyToManyField(Skill)


class Project(models.Model):
    name = models.CharField(max_length=255)
    homepage = models.CharField(max_length=255, default='')
    url = models.CharField(max_length=255, default='')
    description = models.TextField(default='')
    provider = models.CharField(max_length=255)
    external_id = models.CharField(max_length=255)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return '%s: %s' % (self.provider, self.name)
