import pika
import json

class Queue_Client:
  def __init__(self,
    connection: pika.BlockingConnection,
    channel: pika.adapters.blocking_connection.BlockingChannel,
    queue: str):

    self.exchangeName = 'server.queue.' + queue
    self.__connection__ = connection
    self.__channel__ = channel
    self.__channel__.exchange_declare(
      exchange=self.exchangeName,
      exchange_type='fanout'
    )

  def send(self, routing_key: str, dataInput: object):
    try:
      self.__channel__.basic_publish(
        exchange=self.exchangeName,
        routing_key=routing_key,
        properties=pika.BasicProperties(
          content_type='application/json'
        ),
        body=json.dumps(dataInput)
      )
      return {"success":True}
    except pika.exceptions.UnroutableError as error:
      raise error

