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

