#!/usr/bin/env python

# This script starts and waits for messages to come in
# Messages come with the signature:
# { 'method' : 'python_method_to_execute', 'params' : { 'key' : 'value' } }
# Once this is received, the rpc_server.on_request method is invoked
# The rpc_server has a dispatch method
# add to that method any additional methods that need to be supported
import pika
import rpc_server

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

channel = connection.channel()

channel.queue_declare(queue='rpc_queue')

channel.basic_qos(prefetch_count=1)
channel.basic_consume(rpc_server.on_request, queue='rpc_queue')

print " [x] Awaiting RPC requests"
channel.start_consuming()
