from skyamqp import AMQP_Client
import time

connection = AMQP_Client(
  host='192.168.4.100',
  port=5672,
  virtual_host='/',
  username='admin',
  password='123654123',
  heartbeat=5
)

def on_message(dataInput: dict, routing_key: str):
  try:
    # time.sleep(10)
    print(dataInput, routing_key)
  except Exception as e:
    raise e

print('Start')
server = connection.create_Queue_Server(
  queue='test_queue',
  group='group1',
  on_message=on_message,
  prefetch_count=20)

# server.stop()
