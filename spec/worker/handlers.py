"""
Worker handlers for incoming jobs
"""
from django.contrib.auth.models import User
from social.apps.django_app.default.models import UserSocialAuth
from django.db.models import ObjectDoesNotExist
from main.models import Skill, Profile


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
