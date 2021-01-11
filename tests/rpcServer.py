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
  time.sleep(4)
  return 'felhfawhefhwef'

server = connection.create_RPC_Server('test_queue', on_message, 100)

try:
  server.start()
except KeyboardInterrupt as identifier:
  server.stop()