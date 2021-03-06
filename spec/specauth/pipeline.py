"""
Functions to plug into the social auth pipeline
"""
from jobqueue import appserver
from main.models import Profile
from github import Github


def init_github_profile(token, profile):
    github = Github(login_or_token=token)
    data = github.get_user()
    profile.avatar_url = data.avatar_url
    profile.email = data.email
    profile.bio = data.bio
    profile.blog = data.blog
    profile.company = data.company
    profile.location = data.location
    profile.github_url = data.html_url
    profile.github_followers = data.followers
    profile.github_following = data.following
    profile.save()



def create_profile(backend, user, *args, **kwargs):
    """
    create profile model for user
    :param backend:
    :param user:
    :param args:
    :param kwargs:
    :return:
    """
    print('Auth Pipeline: Create profile')
    is_new = kwargs['is_new']
    if not is_new:
        print('Not new user, skip...')
        return
    profile = Profile.objects.create(user=user)
    return {'profile': profile}

def queue_init_profile(backend, user, response, social, new_association, *args, **kwargs):
    """
    queue request to initialize profile data if this is a new user
    or new association for an existing user
    :param backend:
    :param user:
    :param response:
    :param social:
    :param args:
    :param kwargs:
    :return:
    """
    print('Auth Pipeline: Init Profile')
    provider = backend.name
    data = social.extra_data
    token, uid = data['access_token'], data['id']
    print('provider', provider)
    print('social', social)
    print('data', data)
    print('args', kwargs)
    if provider == 'github':
        init_github_profile(token, user.profile)
    appserver.init_user_profile(user.id, provider)
    print('Done')
