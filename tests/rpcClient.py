from skyamqp import AMQP_Client
import time

connection = AMQP_Client(
  host='192.168.4.100',
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
    "data": 1
  })
  print('Done', result)
except Exception as e:
  print('Exception', e)

