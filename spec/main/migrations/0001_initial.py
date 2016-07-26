# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-26 02:59
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=255, null=True)),
                ('bio', models.TextField(default='', null=True)),
                ('blog', models.CharField(max_length=255, null=True)),
                ('company', models.CharField(max_length=255, null=True)),
                ('location', models.CharField(max_length=255, null=True)),
                ('avatar_url', models.CharField(max_length=255, null=True)),
                ('github_url', models.CharField(max_length=255, null=True)),
                ('github_followers', models.IntegerField(null=True)),
                ('github_following', models.IntegerField(null=True)),
                ('overall_score', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ProfileSkill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill_score', models.FloatField(default=0)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('provider', models.CharField(max_length=255)),
                ('external_id', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('homepage', models.CharField(max_length=255, null=True)),
                ('description', models.TextField(null=True)),
                ('private', models.BooleanField(default=False)),
                ('github_url', models.CharField(max_length=255, null=True)),
                ('github_full_name', models.CharField(max_length=255, null=True)),
                ('github_fork', models.BooleanField(default=False)),
                ('github_forks', models.IntegerField(null=True)),
                ('github_stars', models.IntegerField(null=True)),
                ('github_language', models.CharField(max_length=255, null=True)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='RankingResults',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_score', models.FloatField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(default='', null=True)),
                ('max_score', models.FloatField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='skills',
            field=models.ManyToManyField(to='main.Skill'),
        ),
        migrations.AddField(
            model_name='profileskill',
            name='skill',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Skill'),
        ),
        migrations.AddField(
            model_name='profile',
            name='skills',
            field=models.ManyToManyField(through='main.ProfileSkill', to='main.Skill'),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
