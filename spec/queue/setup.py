import os
import pika

connection = pika.BlockingConnection(pika.URLParameters(
        os.environ['CLOUDAMQP_URL']))

channel = connection.channel()


def queue_job(queue, name, data):
    """
    send job to queue
    :param queue: name of the queue
    :param name: name of the job
    :param data: dict containing job payload
    :return:
    """
    print('Sending job', name, 'to queue', queue)
    message = {
        'name': name,
        'data': data
    }
    channel.queue_declare(queue=queue, durable=True)
    channel.basic_publish(
        exchange='',
        routing_key=queue,
        body=message,
        # make message persistent
        properties = pika.BasicProperties(
            delivery_mode=2
        )
    )
