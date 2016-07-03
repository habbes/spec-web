"""
Functions to plug into the social auth pipeline
"""
from jobqueue import hunter


def queue_init_profile(backend, user, response, social, *args, **kwargs):
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
    provider = backend.name
    data = social.extra_data
    token, uid = data['access_token'], data['id']
    print('provider', provider)
    print('social', social)
    print('data', data)
    print('args', kwargs)
    hunter.init_user_profile(provider, uid, token)
    print('Done')
