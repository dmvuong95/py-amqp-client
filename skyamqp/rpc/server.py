import pika

class RPC_Server:
  def __init__(self, connection: pika.BlockingConnection, queue: str, on_message: None, prefetch_count: int):
    self.__customOnMessage__ = on_message
    self.__channel__ = connection.channel()
    self.__channel__.basic_qos(prefetch_count=(prefetch_count or 100))
    self.queueName = 'server.rpc.' + queue
    self.__channel__.queue_declare(queue=self.queueName)
    self.__channel__.basic_consume(
      queue=self.queueName,
      on_message_callback=self.__on_message__
    )
  def __on_message__(
    self,
    channel: pika.adapters.blocking_connection.BlockingChannel,
    method: pika.spec.Basic.Deliver,
    properties: pika.spec.BasicProperties,
    body: bytes):
    # print(method.delivery_tag, method.routing_key, properties.content_type)
    response = self.__customOnMessage__(body, method.routing_key)
    channel.basic_publish(
      exchange='',
      routing_key=properties.reply_to,
      body=response,
      properties=pika.BasicProperties(correlation_id=properties.correlation_id)
    )
    channel.basic_ack(delivery_tag=method.delivery_tag)

  def stop(self):
    self.__channel__.stop_consuming()
  def start(self):
    self.__channel__.start_consuming()
