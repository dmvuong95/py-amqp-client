# RPC Client
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

client = connection.create_RPC_Client(
  queue='test_queue',
  timeout=0)
try:
  result = client.send('routing.key.test', 'sample message')
  print('Result:', result)
except Exception as e:
  print(e)

```
# RPC Server
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

def on_message(data, routing_key):
  # Logic code here
  return 'result for client here'

server = connection.create_RPC_Server(
  queue='test_queue',
  on_message=on_message,
  prefetch_count=100)

try:
  server.start()
except KeyboardInterrupt as identifier:
  server.stop()
```
