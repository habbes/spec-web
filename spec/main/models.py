from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Skill(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(default='', null=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    skills = models.ManyToManyField(Skill)
    email = models.CharField(max_length=255, null=True)
    bio = models.TextField(default='', null=True)
    blog = models.CharField(max_length=255, null=True)
    company = models.CharField(max_length=255, null=True)
    location = models.CharField(max_length=255, null=True)
    avatar_url = models.CharField(max_length=255, null=True)
    github_url = models.CharField(max_length=255, null=True)
    github_followers = models.IntegerField(null=True,)
    github_following = models.IntegerField(null=True)


class Project(models.Model):
    skills = models.ManyToManyField(Skill)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    provider = models.CharField(max_length=255)
    external_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    homepage = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    private = models.BooleanField(default=False)
    github_url = models.CharField(max_length=255, null=True)
    github_full_name = models.CharField(max_length=255, null=True)
    github_fork = models.BooleanField(default=False)
    github_forks = models.IntegerField(null=True)
    github_stars = models.IntegerField(null=True)
    github_language = models.CharField(max_length=255, null=True)

    def __str__(self):
        return '%s: %s' % (self.provider, self.name)
