#!/usr/bin/env python
import pika

def printing_line_callback(line):
    print(line)

class RabbitMQ:
    """Class for sending or receiving on a RabbitMQ queue.

    To send:
        rmq = RabbitMQ("localhost", "test_queue")
        rmq.send("this is a test message, any string is fine")

    To receive (runs forever):
        rmq = RabbitMQ("localhost", "test_queue")
        def line_callback(line):
            print("I got this line from test_queue: {}".format(line)
        rmq.receive(line_callback)
    """
    def __init__(self, host, queue, line_callback=printing_line_callback):
        print("RabbitMQ created for {}:{}".format(host,queue))
        self.host = host
        self.queue = queue
        self.send_callback = self.default_send_callback
        self.receive_callback = self.default_receive_callback
        self.line_callback = line_callback

    def default_send_callback(self, message):
        print(" [x] Sent '{}'".format(message))

    def default_receive_callback(self, ch, method, properties, body):
        """
        :param ch: dunno
        :param method: dunno
        :param properties: dunno
        :param body: the message received via rabbitmq, for this code it is
         a string -- a line of text.  We call the 'line_callback' passed into
         this instance, and pass in the text line received.
        :return: N/A
        """
        print(" [x] Received '{}'".format(body.decode("utf-8").strip()))
        self.line_callback(body.decode("utf-8").strip())

    def send(self, message):
        #print("RabbitMQ should send: {}".format(message))
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
        channel = connection.channel()

        channel.queue_declare(queue=self.queue)

        channel.basic_publish(exchange='',
                          routing_key=self.queue,
                          body=message)
        self.send_callback(message)

        connection.close()

    def receive(self, line_processor=None):
        self.line_callback = line_processor
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
        channel = connection.channel()

        channel.queue_declare(queue=self.queue)

        channel.basic_consume(self.receive_callback,
                          queue=self.queue,
                          no_ack=True)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()


