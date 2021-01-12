import pika
import uuid
import time
from skyamqp.rpc import RPC_Server, RPC_Client

class AMQP_Client:
  def __init__(self, host, port, virtual_host, username, password, heartbeat):
    self.__connection__ = pika.BlockingConnection(
      pika.ConnectionParameters(
        host=host,
        port=port,
        virtual_host=virtual_host,
        heartbeat=heartbeat,
        credentials=pika.PlainCredentials(username, password)
      )
    )
  
  def create_RPC_Server(self, queue: str, on_message: None, prefetch_count: int):
    return RPC_Server(self.__connection__, queue, on_message, prefetch_count)
  def create_RPC_Client(self, queue: str, timeout: int = 0):
    if not hasattr(self, "__clientChannel__"):
      self.__clientChannel__ = self.__connection__.channel()
      self.__clientChannel__.confirm_delivery()
    return RPC_Client(self.__connection__, self.__clientChannel__, queue, timeout)
