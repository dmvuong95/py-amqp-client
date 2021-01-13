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

def on_message(dataInput: object, routing_key: str):
  print(routing_key, dataInput)
  time.sleep(10)
  print('OK')
  return {"success": True}

server = connection.create_Queue_Server(
  queue='test_queue',
  group='group2',
  on_message=on_message,
  prefetch_count=30)

try:
  server.start()
except KeyboardInterrupt as identifier:
  server.stop()