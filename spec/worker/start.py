"""
Asynchronous worker to fetch incoming jobs from queue
"""
import pika
import os
import json
import dotenv
dotenv.read_dotenv(os.path.join('..', '.env'))
from django.conf import settings
import spec.spec
import spec.spec.settings
settings.configure(spec.spec.settings)

import handlers

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
    if handler: handler(data)
    channel.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == '__main__':
    print('Worker started...')
    fetch_jobs(QUEUE, callback)
    print('Fetching jobs...')
