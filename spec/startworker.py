"""
Asynchronous worker to fetch incoming jobs from queue
"""
import pika
import os
import json
import dotenv
dotenv.read_dotenv()
from django.conf import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spec.settings')
from django.apps import apps
apps.populate(settings.INSTALLED_APPS)

from worker import handlers

QUEUE = 'appserver_queue'






def fetch_jobs(queue, callback):
    connection = pika.BlockingConnection(pika.URLParameters(
        os.environ['CLOUDAMQP_URL']))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE, durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(callback, queue=queue)
    channel.start_consuming()


def get_handler(name):
    if name == 'projectSkills':
        return handlers.project_skills
    if name == 'initUserProfile':
        return handlers.init_user_profile

def callback(channel, method, properties, body):
    print('Incoming message received')
    msg = json.loads(body.decode('utf-8'))
    name, data = msg['name'], msg['data']
    print('Job Name', name)
    print('Job Data', data)
    handler = get_handler(name)
    if handler:
        print('Handler found, exectuing handler...')
        try:
            handler(data)
            print('Job complete')
            channel.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print('Job failed on error', e)



if __name__ == '__main__':
    print('Worker started...')
    print('Fetching jobs...')
    fetch_jobs(QUEUE, callback)
