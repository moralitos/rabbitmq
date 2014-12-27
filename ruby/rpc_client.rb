require 'bunny'
require 'thread'
require 'securerandom'
require 'json'

# This class wraps abstracts all the connection code
# and just exposes a class method called execute that will handle
# the call to python and get the response
class RpcClient
  # The execute method is the only method that should be used
  # pass a request hash with the signature
  # RpcClient.execute(method: 'python_method_name', params: { key: 'value', key2: 'value2' }
  def self.execute(request = { method: 'the_pyton_method_name', params: { key: 'value', another_key: 'another_value' } })
    client = RpcClient.new
    client.execute(request.to_json) # convert the hash to json before passing to the instance method execute
  end

  # RpcClient Implementation
  #
  # the channel uses the connection class method
  # starts the connection and creates the channel
  # we are only using one channel
  def self.channel
    @channel ||=
      begin
        connection.start
        connection.create_channel
      end
  end

  # make this a class method, a singleton to only have one
  # connection
  def self.connection
    @connection ||= Bunny.new(automatically_recover: false)
  end

  attr_reader :reply_queue
  attr_accessor :response, :call_id
  attr_reader :lock, :condition

  def initialize
    @lock      = Mutex.new
    @condition = ConditionVariable.new
  end

  def exchange
    @exchange ||= RpcClient.channel.default_exchange
  end

  def server_queue
    'rpc_queue' # this name needs to match the python side name
  end

  def reply_queue
    @reply_queue ||=
      begin
        queue = RpcClient.channel.queue('', exclusive: true)
        subscribe(queue) # subscribe the reply queue as soon as we set it
        queue
      end
  end

  def subscribe(queue)
    that = self
    queue.subscribe do |_delivery_info, properties, payload|
      if properties[:correlation_id] == that.call_id
        that.response = JSON.parse(payload) # convert the string we receive back to a ruby hash from json
        that.lock.synchronize { that.condition.signal }
      end
    end
  end

  def execute(json_request)
    self.call_id = generate_uuid

    exchange.publish(json_request,
                     routing_key: server_queue,
                     correlation_id: call_id,
                     reply_to: reply_queue.name)

    lock.synchronize { condition.wait(lock) }
    response
  end

  protected

  def generate_uuid
    SecureRandom.uuid
  end
end
