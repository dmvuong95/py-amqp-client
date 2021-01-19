from skyamqp import AMQP_Client
import time

connection = AMQP_Client(
  host='192.168.4.121',
  username='admin',
  password='123654123',
  virtual_host='/',
  port=5672,
  heartbeat=5
)

client = connection.create_RPC_Client(
  queue='test_queue',
  timeout=5)
try:
  # time.sleep(15)
  result = client.send('routing.key.test', {
    "data": '123'
  })
  print('Result:', result)
  time.sleep(20)
  result = client.send('routing.key.test', {
    "data": '456'
  })
  print('Result:', result)
except Exception as e:
  print('Exception', e)

