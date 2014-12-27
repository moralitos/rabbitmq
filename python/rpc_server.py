import pika
import json
import concatenate

# This is the method that gets modified as we add more methods
# match the string and then call your specific functionality
# the example here, imports the module concatenate, and it users its concat
# method to provide the ability to concatenate strings
def dispatch(message):
    method = message['method'] # the message has been parsed from json by the on_request method
    params = message['params']

    if method == 'concatenate':
        return concatenate.concat(params)
    else:
        return { status: 'error', error: 'method does not exist' }

def on_request(ch, method, props, message_body):

    print " [.] received: "  + message_body

    response = dispatch(json.loads(message_body))
    json_response = json.dumps(response)
    print " [.] sending: " + json_response

    ch.basic_publish(exchange='',
            routing_key=props.reply_to,
            body= json_response, # encode it to json before sending back to ruby
            properties=pika.BasicProperties(correlation_id = props.correlation_id))

    ch.basic_ack(delivery_tag = method.delivery_tag)


