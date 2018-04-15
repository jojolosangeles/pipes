#!/usr/bin/env python
import pika

class RabbitMQ:
    def __init__(self, host, queue):
        self.host = host
        self.queue = queue
        self.send_callback = self.default_send_callback
        self.receive_callback = self.default_receive_callback

    def default_send_callback(self, message):
        print(" [x] Sent '{}'".format(message))

    def default_receive_callback(self, ch, method, properties, body):
        print(" [x] Received %r" % body)

    def send(self, message):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
        channel = connection.channel()

        channel.queue_declare(queue=self.queue)

        channel.basic_publish(exchange='',
                          routing_key=self.queue,
                          body=message)
        self.send_callback(message)

        connection.close()

    def receive(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
        channel = connection.channel()

        channel.queue_declare(queue=self.queue)

        channel.basic_consume(self.receive_callback,
                          queue=self.queue,
                          no_ack=True)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
