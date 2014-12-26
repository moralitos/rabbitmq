#!/usr/bin/env python
import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

channel = connection.channel()

channel.queue_declare(queue='rpc_queue')

def fib(params):
    if params['number']:
        return { status: 'success', params: { answer: 'this is the answer' } }
    else:
        return { status: 'error', error: 'expected to receive a number in the params' }

def dispatch(message):
    method = message['method'] # the message has been parsed from json by the on_request method
    params = message['params']

    if method == 'fib':
        return fib(params)
    else:
        return { status: 'error', error: 'method does not exist' }

def on_request(ch, method, props, message_body):

    print " [.] received: "  + message_body

    response_body = dispatch(json.loads(message_body))

    ch.basic_publish(exchange='',
            routing_key=props.reply_to,
            body= json.dumps(response_body), # encode it to json before sending back to ruby
            properties=pika.BasicProperties(correlation_id = props.correlation_id))

    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='rpc_queue')

print " [x] Awaiting RPC requests"
channel.start_consuming()

