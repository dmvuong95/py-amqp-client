from skyamqp import AMQP_Client

connection = AMQP_Client(
  host='192.168.4.107',
  port=5672,
  virtual_host='/',
  username='admin',
  password='123654123',
  heartbeat=5
)

client = connection.create_Queue_Client(
  queue='test_queue')
try:
  for i in range(100):
    result = client.send('routing.key.test', {
      "data": str(i)
    })
    print('Result:', result, i)
    pass
except Exception as e:
  print(e)

