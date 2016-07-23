from .setup import queue_job

QUEUE = 'appserver_queue'

INIT_USER_PROFILE = 'initUserProfile'


def job(name, data):
    queue_job(QUEUE, name, data)


def init_user_profile(user_id, provider):
    data = {
        'userId': user_id,
        'provider': provider
    }
    job(INIT_USER_PROFILE, data)


