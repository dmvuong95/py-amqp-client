# Upload package to Pypiserver
Set Pypiserver host in `.pypirc`
```conf
[local]
repository: http://192.168.4.100:5002
username: admin
password: 123654123

[distutils]
index-servers =
  local
```
Build and upload package to Pypiserver
```bash
$ bash script-build.sh
```
# Install package from Pypiserver
When pip search packages, pip will read the configuration in `~/.pip/pip.conf`
Make custom configuration `~/.pip/pip.conf`:
```conf
[global]
extra-index-url = http://192.168.4.100:5002/simple/
trusted-host = 192.168.4.100
```
Install now:
```bash
$ pip install skyamqp
```

# Init connection to RabbitMQ
```python
from skyamqp import AMQP_Client

connection = AMQP_Client(
  host='192.168.4.107',
  port=5672,
  virtual_host='/eof',
  username='admin',
  password='123654123',
  heartbeat=5
)
```
# RPC
## RPC Client
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
## RPC Server
```python
def on_message(dataInput: dict, routing_key: str):
  # Logic code here
  # Must to return object json
  return {"success": True}

try:
  server = connection.create_RPC_Server(
    queue='test_rpc',
    on_message=on_message,
    prefetch_count=100)

except KeyboardInterrupt:
  server.stop()
```
# Queue
## Queue Client
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
## Queue Server
```python
def on_message(dataInput: dict, routing_key: str):
  try:
    # Logic code here
    # Return nothing
  except Exception as e:
    # raise exception to un-ack and requeue message
    raise e

try:
  server = connection.create_Queue_Server(
    queue='test_queue',
    group='group1',
    on_message=on_message,
    prefetch_count=100)

except KeyboardInterrupt:
  server.stop()
```
