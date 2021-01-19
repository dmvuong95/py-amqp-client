import pika
import json

class Queue_Client_Thread:
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

  def send(self, args: dict):
    routing_key: str = args['routing_key']
    dataInput: dict = args['dataInput']
    try:
      self.__channel__.basic_publish(
        exchange=self.exchangeName,
        routing_key=routing_key,
        properties=pika.BasicProperties(
          content_type='application/json'
        ),
        body=json.dumps(dataInput)
      )
      args['response'] = {"success":True}
    except pika.exceptions.UnroutableError as error:
      args['exception'] = error

