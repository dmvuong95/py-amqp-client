from skyamqp import AMQP_Client
import time

connection = AMQP_Client(
  host='192.168.4.107',
  port=5672,
  virtual_host='/',
  username='admin',
  password='123654123',
  heartbeat=5
)

def on_message(data, routing_key):
  print(routing_key, data)
  for i in range(10000000):
    print(i)
  return 'felhfawhefhwef'

server = connection.create_RPC_Server(
  queue='test_queue',
  on_message=on_message,
  prefetch_count=100)

try:
  server.start()
except KeyboardInterrupt as identifier:
  server.stop()