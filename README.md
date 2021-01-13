# Init connection
```python
from skyamqp import AMQP_Client

connection = AMQP_Client(
  host='192.168.4.107',
  port=5672,
  virtual_host='/',
  username='admin',
  password='123654123',
  heartbeat=5
)
```
# RPC
## Client
```python
client = connection.create_RPC_Client(
  queue='test_rpc',
  timeout=0)
try:
  # Must to send object json
  result = client.send('routing.key.test', {
    "data": '123'
  })
  print('Result:', result)
except Exception as e:
  print(e)

```
## Server
```python
def on_message(dataInput: object, routing_key: str):
  # Logic code here
  # Must to return object json
  return {"success": True}

server = connection.create_RPC_Server(
  queue='test_rpc',
  on_message=on_message,
  prefetch_count=100)

try:
  server.start()
except KeyboardInterrupt as identifier:
  server.stop()
```
# Queue
## Client
```python
client = connection.create_Queue_Client(
  queue='test_queue')
try:
  client.send('routing.key.test', {
    "data": '456'
  })
  print('Sent!!')
except Exception as e:
  print(e)
```
## Server
```python
def on_message(dataInput: object, routing_key: str):
  try:
    # Logic code here
    # Return nothing
  except Exception as e:
    # raise exception to un-ack and requeue message
    raise e

server = connection.create_Queue_Server(
  queue='test_queue',
  group='group1',
  on_message=on_message,
  prefetch_count=100)

try:
  server.start()
except KeyboardInterrupt as identifier:
  server.stop()
```
