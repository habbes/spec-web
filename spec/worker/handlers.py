"""
Worker handlers for incoming jobs
"""
from django.contrib.auth.models import User
from social.apps.django_app.default.models import UserSocialAuth
from django.db.models import ObjectDoesNotExist
from github import Github
from main.models import Skill, Profile, ProfileSkill
from . import ranking
from jobqueue import appserver


def get_object_or_null(klass, *args, **kwargs):
    try:
        return klass.get(*args, **kwargs)
    except ObjectDoesNotExist as e:
        print(e)
        return

def project_skills(data):
    print('Handling job: projectSkills')
    uid, projects, skills = \
        data['userId'], data['projects'], data['skills']
    provider='github'
    social = get_object_or_null(UserSocialAuth.objects, provider=provider, uid=uid)
    if not social:
        print('Social Auth not found', provider, uid)
        return
    user = social.user
    if not user:
        print('User %s not found')
        return
    try:
        profile = user.profile
    except ObjectDoesNotExist:
        profile = Profile.objects.create(user=user)
    print('Adding skills')
    for skill in skills:
        print('Skill', skill)
        if not skill:
            # skill is none
            continue
        sk = get_object_or_null(Skill.objects, name=skill)
        if sk:
            # if skill exist, add to profile
            # if user doesn't have skill already
            p_sk = get_object_or_null(profile.skills, id=sk.id)
            if not p_sk:
                print('Associate existing skill')
                profile.skills.add(sk)
        else:
            # if skill doesn't exist create it
            print('Create new skill')
            profile.skills.create(name=skill)
    print('Finished add skills')
    print('Adding projects')
    for project in projects:
        provider, external_id = project['provider'], project['externalId']
        print('Project', provider, external_id)
        p_proj = get_object_or_null(profile.project_set, provider=provider, external_id=external_id)
        if p_proj:
            # Skip project if already exists
            print('Already has project')
            continue
        profile.project_set.create(
            provider=provider,
            external_id=external_id,
            name=project['name'],
            url=project['url'],
            language=project['language'],
            description=project['description'],
            homepage=project['homepage']
        )


def init_user_profile(data):
    print('handling job init_user_profiles')
    uid, provider = \
        data['userId'], data['provider']
    user = User.objects.get(id=uid)
    if provider == 'github':
        init_user_github_profile(user)
    # queue job to rank profiles
    appserver.rank_profiles()


def init_user_github_profile(user):
    print('init user github profile')
    provider = 'github'
    social = UserSocialAuth.objects.get(provider=provider, user_id = user.id)
    profile = user.profile
    token = social.extra_data['access_token']
    github = Github(login_or_token=token)
    github_user = github.get_user()
    repos = github_user.get_repos()
    for repo in repos:
        print('repo', repo.name)
        project = profile.project_set.create()
        project.provider = provider
        project.external_id = repo.id
        project.name = repo.name
        project.homepage = repo.homepage
        project.description = repo.description
        project.private = repo.private
        project.github_url = repo.html_url
        project.github_full_name = repo.full_name
        project.github_fork = repo.fork
        project.github_forks = repo.forks_count
        project.github_stars = repo.stargazers_count
        project.github_language = repo.language
        project.save()
        languages = repo.get_languages().keys()
        for lang in languages:
            print('skill', lang)
            if not lang: continue
            sk = get_object_or_null(Skill.objects, name=lang)
            if not sk:
                sk = Skill.objects.create(name=lang)

            # create profile_skill if it doesn't exist
            # TODO: Use transaction or db constraints instead of lookup+update
            try:
                ProfileSkill.objects.get(profile=profile, skill=sk)
            except ObjectDoesNotExist as e:
                ProfileSkill.objects.create(profile=profile, skill=sk)
            project.skills.add(sk)


def rank_profiles(data):
    ranking.rank_profiles()