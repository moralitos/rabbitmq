Ruby to Python RPC with RabbitMQ
--------------------------------

This is an expansion on the rabbitmq tutorial to create a Remote Procedure Call (RPC) from ruby to python
(ruby is the client and python is the RPC server).

This uses the ruby example and separates business logic from low level connections
and does the same for the python server side.

## To use this from ruby side:

  ```
RpcClient.execute(method: 'concatenate', params: { strings: ['con', 'ca', 'te', 'na', 'tion'] })
  ```

## Prerequisites:

  * rabbitmq server
  * python
  * ruby
  * gem rspec
  * gem bunny

## Testing:

  * start the rabbit mq server
  ```
  $ rabbitmq-server
  ```

  * start the python rpc server
  ```
  $ cd python
  $ python rpc_server.py
  ```

  * run the spec
  ```
  $ cd ruby
  $ rspec rpc_client_spec.rb
  ```
