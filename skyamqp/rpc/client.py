import pika
import uuid
import time
import json

class RPC_Client_Thread:
  def __init__(self, connection: pika.BlockingConnection, channel: pika.adapters.blocking_connection.BlockingChannel, queue: str, timeout: int = 0):
    self.__responses__ = []
    self.__timeout__ = timeout

    self.queueName = 'server.rpc.' + queue
    self.__connection__ = connection
    self.__channel__ = channel
    # Consume an exclusive queue
    resultQueueDeclare = self.__channel__.queue_declare(
      queue='',
      exclusive=True
    )
    self.__cbQueueName__ = resultQueueDeclare.method.queue
    self.__channel__.basic_consume(
      queue=self.__cbQueueName__,
      auto_ack=True,
      on_message_callback=self.__on_message__
    )
    # Bind exchange to queue
    self.__channel__.queue_declare(self.queueName)
    self.__channel__.exchange_declare(
      exchange=self.queueName,
      exchange_type='fanout'
    )
    self.__channel__.queue_bind(
      queue=self.queueName,
      exchange=self.queueName,
    )

  def send(self, args: dict):
    routing_key: str = args['routing_key']
    dataInput: dict = args['dataInput']
    result = self.__channel__.queue_declare(self.queueName)
    if int(result.method.consumer_count) == 0:
      args['exception'] = 'NO_SERVER_AVAILABLE'
      return
    
    self.__responses__.append(args)
    try:
      self.__channel__.basic_publish(
        exchange=self.queueName,
        routing_key=routing_key,
        properties=pika.BasicProperties(
          correlation_id=args['corr_id'],
          reply_to=self.__cbQueueName__,
          content_type='application/json'
        ),
        body=json.dumps(dataInput)
      )
    except pika.exceptions.UnroutableError as error:
      args['exception'] = error
      return

    # t = time.time()
    # while ((res.response is None) and (self.__timeout__ == 0 or time.time() - t < self.__timeout__)):
    #   self.__connection__.process_data_events()
    # self.__responses__.remove(res)
    # if res.response is None:
    #   args['exception'] = 'REQUEST_WAS_TIMED_OUT'
    #   return
    # return res.response

  def __on_message__(
    self,
    channel: pika.adapters.blocking_connection.BlockingChannel,
    method: pika.spec.Basic.Deliver,
    properties: pika.spec.BasicProperties,
    body: bytes):
    # print(method.delivery_tag, method.routing_key)
    # print(properties.content_type, properties.correlation_id)
    # print(body)
    for res in self.__responses__:
      if res['corr_id'] == properties.correlation_id:
        res['response'] = json.loads(body)
        self.__responses__.remove(res)
        break

