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
  try:
    time.sleep(10)
    print('OK')
  except Exception as e:
    raise e

server = connection.create_Queue_Server(
  queue='test_queue',
  group='group1',
  on_message=on_message,
  prefetch_count=20)

try:
  server.start()
except KeyboardInterrupt as identifier:
  server.stop()