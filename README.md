Ruby to Python RPC with RabbitMQ
--------------------------------

This is an expansion on the rabbitmq tutorial to create an RPC connection.

This uses the ruby example and separates business logic from low level connections
and does the same for the python server side.

## To use this from ruby side:

```
RpcClient.execute(some_number)
```

## Prerequisites:

* rabbitmq server
* python
* ruby
    rspec
    bunny

## Running:

* start the rabbit mq server
```
$ rabbitmq-server
```

* run the spec
```
$ rspec rpc_client_spec.rb
```
