from .setup import queue_job

QUEUE = 'hunter_queue'

INIT_USER_PROFILE = 'initUserProfile'


def job(name, data):
    queue_job(QUEUE, name, data)


def init_user_profile(provider, user_id, access_token):
    data = {
        'userId': user_id,
        'accessToken': access_token,
        'provider': provider
    }
    job(INIT_USER_PROFILE, data)


