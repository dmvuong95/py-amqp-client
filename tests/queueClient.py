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

client = connection.create_Queue_Client(
  queue='test_queue')
# time.sleep(10)
try:
  for i in range(500000):
    result = client.send('routing.key.test', {
      "data": str(i)
    })
    print('Result:', result, i)
    pass
except Exception as e:
  print(e)

