"""
Functions to plug into the social auth pipeline
"""
from jobqueue import hunter
from main.models import Profile


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
    profile = Profile.create(user=user)
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
    if not new_association:
        print('Not new association, skip...')
        return
    provider = backend.name
    data = social.extra_data
    token, uid = data['access_token'], data['id']
    print('provider', provider)
    print('social', social)
    print('data', data)
    print('args', kwargs)
    hunter.init_user_profile(provider, uid, token)
    print('Done')
