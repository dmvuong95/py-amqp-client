from skyamqp import AMQP_Client
import time

connection = AMQP_Client(
  host='192.168.4.100',
  username='admin',
  password='123654123',
  virtual_host='/',
  port=5672,
  heartbeat=5,
)

def on_message(dataInput: dict, routing_key: str):
  print(routing_key, dataInput)
  time.sleep(dataInput['data'])
  # for i in range(10000):
  #   t = {
  #     'a': 1
  #   }
  #   print(t)
  return {"success": True}

print('starting')
server = connection.create_RPC_Server(
  queue='test_queue',
  on_message=on_message,
  prefetch_count=1000)
print('started')
# time.sleep(20)
# print("sleep done")
# server.stop()
# try:
#   server.start()
# except KeyboardInterrupt as identifier:
#   server.stop()
#   pass
