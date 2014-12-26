#!/usr/bin/env python
import pika
import json

class RpcServer:
  def connection(self):
    return pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

  def channel(self):
    channel = self.connection().channel()
    channel.queue_declare(queue='rpc_queue') # this is the matching queue with ruby client
    return channel

  def concatenate(self, params):
    if params['strings']:
      strings = params['strings']
      concatenated_string = ''
      for string in strings:
        concatenated_string += string
      return { 'status' : 'success', 'params' : { 'answer' : concatenated_string } }
    else:
      return { 'status' : 'error', 'error' : 'expected to receive a number in the params' }

  def dispatch(self, message):
      print message
      method = message['method'] # the message has been parsed from json by the on_request method
      params = message['params']

      if method == 'concatenate':
          return concatenate(params)
      else:
          return { 'status' : 'error', 'error' : 'method does not exist' }

  def on_request(self, ch, method, props, message_body):

      print " [.] received: "  + message_body

      response_body = dispatch(json.loads(message_body))

      ch.basic_publish(exchange='',
              routing_key=props.reply_to,
              body= json.dumps(response_body), # encode it to json before sending back to ruby
              properties=pika.BasicProperties(correlation_id = props.correlation_id))

      ch.basic_ack(delivery_tag = method.delivery_tag)

  def start(self):
    self.channel().basic_qos(prefetch_count=1)
    self.channel().basic_consume(self.on_request, queue='rpc_queue')
    print "awaiting RPC requests"
    self.channel().start_consuming()

