#!/usr/bin/env python
import pika
import sys

queue_name = sys.argv[1]
message = sys.argv[2]
print("queue_name={}".format(queue_name))
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()


channel.queue_declare(queue=queue_name)

channel.basic_publish(exchange='',
                      routing_key=queue_name,
                      body=message)
print(" [x] Sent '{}'".format(message))
connection.close()