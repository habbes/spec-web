"""
Asynchronous worker to fetch incoming jobs from queue
"""
import pika
import os
import json
import dotenv

QUEUE = 'appserver_queue'

dotenv.read_dotenv(os.path.join('..', '.env'))


def fetch_jobs(queue, callback):
    connection = pika.BlockingConnection(pika.URLParameters(
        os.environ['CLOUDAMQP_URL']))
    channel = connection.channel()

    channel.queue_declare(queue=QUEUE, durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(callback, queue=queue)
    channel.start_consuming()


def callback(channel, method, properties, body):
    print('Incoming message received')
    msg = json.loads(body.decode('utf-8'))
    name, data = msg['name'], msg['data']
    print('Job Name', name)
    print('Job Data', data)
    channel.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == '__main__':
    print('Worker started...')
    fetch_jobs(QUEUE, callback)
    print('Fetching jobs...')
