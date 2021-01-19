import pika
import functools
import threading
import json

class RPC_Server_Thread:
  def __init__(self, connection: pika.BlockingConnection, queue: str, on_message: None, prefetch_count: int):
    self.__channel__ = connection.channel()
    self.__channel__.basic_qos(prefetch_count=(prefetch_count or 100))
    self.queueName = 'server.rpc.' + queue
    self.__channel__.queue_declare(queue=self.queueName)
    self.__threads__ = []
    on_message_callback = functools.partial(on_message_global, args=(connection, self.__threads__, on_message))
    self.__channel__.basic_consume(
      queue=self.queueName,
      on_message_callback=on_message_callback
    )

  def stop(self):
    self.__channel__.stop_consuming()
    for thread in self.__threads__:
      thread.join()

def do_work(
  conn: pika.BlockingConnection,
  channel: pika.adapters.blocking_connection.BlockingChannel,
  method: pika.spec.Basic.Deliver,
  properties: pika.spec.BasicProperties,
  body: bytes,
  custom_func):
  try:
    response = custom_func(json.loads(body), method.routing_key)
    conn.add_callback_threadsafe(functools.partial(send_response, channel, properties, json.dumps(response)))
    conn.add_callback_threadsafe(functools.partial(ack_message, channel, method.delivery_tag))
  except Exception as e:
    print(e)
    conn.add_callback_threadsafe(functools.partial(nack_message, channel, method.delivery_tag))

def on_message_global(
  channel: pika.adapters.blocking_connection.BlockingChannel,
  method: pika.spec.Basic.Deliver,
  properties: pika.spec.BasicProperties,
  body: bytes,
  args):
  (conn, thrds, custom_func) = args
  t = threading.Thread(target=do_work, args=(conn, channel, method, properties, body, custom_func))
  t.start()
  thrds.append(t)

def ack_message(ch: pika.adapters.blocking_connection.BlockingChannel, delivery_tag):
  """Note that `ch` must be the same pika channel instance via which
  the message being ACKed was retrieved (AMQP protocol constraint).
  """
  if ch.is_open:
    ch.basic_ack(delivery_tag)
  else:
    # Channel is already closed, so we can't ACK this message;
    # log and/or do something that makes sense for your app in this case.
    pass

def nack_message(ch: pika.adapters.blocking_connection.BlockingChannel, delivery_tag):
  if ch.is_open:
    ch.basic_nack(delivery_tag)
  else:
    pass

def send_response(
  channel: pika.adapters.blocking_connection.BlockingChannel,
  properties: pika.spec.BasicProperties,
  response):
  channel.basic_publish(
    exchange='',
    routing_key=properties.reply_to,
    body=response,
    properties=pika.BasicProperties(correlation_id=properties.correlation_id)
  )
