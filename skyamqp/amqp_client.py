import pika
from skyamqp.rpc import RPC_Server_Thread, RPC_Client_Thread
from skyamqp.queue import Queue_Server_Thread, Queue_Client_Thread
import threading
import uuid
import time
import logging
logger = logging.getLogger('skyamqp')

class AMQP_Client:
  __queueCmd__ = []
  def __init__(self, host, username, password, virtual_host: str = '/', port: int = 5672, heartbeat: int = 0):
    self.__connectionId__ = str(uuid.uuid4())
    threading.Thread(target=self.__create_thread, args=(host, username, password, virtual_host, port, heartbeat)).start()
  
  def create_RPC_Server(self, queue: str, on_message: None, prefetch_count: int):
    rpcServerId = str(uuid.uuid4())
    self.__queueCmd__.append({
      "method": "create_RPC_Server",
      "args": {
        "queue": queue,
        "on_message": on_message,
        "prefetch_count": prefetch_count,
        "id": rpcServerId
      }
    })
    return RPC_Server(rpcServerId, queue, self.__queueCmd__)
    
  def create_RPC_Client(self, queue: str, timeout: int = 0):
    rpcClientId = str(uuid.uuid4())
    self.__queueCmd__.append({
      "method": "create_RPC_Client",
      "args": {
        "queue": queue,
        "timeout": timeout,
        "id": rpcClientId
      }
    })
    return RPC_Client(rpcClientId, queue, self.__queueCmd__, timeout)

  def create_Queue_Server(self, queue: str, group: str, on_message: None, prefetch_count: int):
    queueServerId = str(uuid.uuid4())
    self.__queueCmd__.append({
      "method": "create_Queue_Server",
      "args": {
        "queue": queue,
        "group": group,
        "on_message": on_message,
        "prefetch_count": prefetch_count,
        "id": queueServerId
      }
    })
    return Queue_Server(queueServerId, queue, self.__queueCmd__)
  
  def create_Queue_Client(self, queue: str):
    queueClientId = str(uuid.uuid4())
    self.__queueCmd__.append({
      "method": "create_Queue_Client",
      "args": {
        "queue": queue,
        "id": queueClientId
      }
    })
    return Queue_Client(queueClientId, queue, self.__queueCmd__)

  def __create_thread(self, host, username, password, virtual_host, port, heartbeat):
    connection = AMQP_Client_Thread(host, username, password, virtual_host, port, heartbeat)
    rpcServerList = {}
    rpcClientList = {}
    queueServerList = {}
    queueClientList = {}
    listCmd = {}
    while True:
      # print(1)
      if len(self.__queueCmd__):
        cmd = self.__queueCmd__[0]
        # print(4444, cmd)
        # RPC
        if cmd['method'] == 'create_RPC_Server':
          rpcServer = connection.create_RPC_Server(cmd['args']['queue'], cmd['args']['on_message'], cmd['args']['prefetch_count'])
          rpcServerList[cmd['args']['id']] = rpcServer
          listCmd[cmd['args']['id']] = cmd
        if cmd['method'] == 'RPC_Server.stop':
          rpcServerList[cmd['args']['id']].stop()
          listCmd[cmd['args']['id']] = None
        
        if cmd['method'] == 'create_RPC_Client':
          rpcClient = connection.create_RPC_Client(cmd['args']['queue'], cmd['args']['timeout'])
          rpcClientList[cmd['args']['id']] = rpcClient
          listCmd[cmd['args']['id']] = cmd
        if cmd['method'] == 'RPC_Client.send':
          rpcClientList[cmd['args']['id']].send(cmd['args'])

        # Queue
        if cmd['method'] == 'create_Queue_Server':
          queueServer = connection.create_Queue_Server(cmd['args']['queue'], cmd['args']['group'], cmd['args']['on_message'], cmd['args']['prefetch_count'])
          queueServerList[cmd['args']['id']] = queueServer
          listCmd[cmd['args']['id']] = cmd
        if cmd['method'] == 'Queue_Server.stop':
          queueServerList[cmd['args']['id']].stop()
          listCmd[cmd['args']['id']] = None

        if cmd['method'] == 'create_Queue_Client':
          queueClient = connection.create_Queue_Client(cmd['args']['queue'])
          queueClientList[cmd['args']['id']] = queueClient
          listCmd[cmd['args']['id']] = cmd
        if cmd['method'] == 'Queue_Client.send':
          queueClientList[cmd['args']['id']].send(cmd['args'])
        
        self.__queueCmd__.remove(cmd)
        pass
      else:
        try:
          connection.__connection__.process_data_events(0.2)
          pass
        except pika.exceptions.StreamLostError as e:
          logger.warning(e)
          # re-connect
          if connection.__connection__.is_open:
            connection.__connection__.close()
          time.sleep(0.2)
          connection = AMQP_Client_Thread(host, username, password, virtual_host, port, heartbeat)
          for key in listCmd:
            if listCmd[key] is None:
              pass
            else:
              self.__queueCmd__.append(listCmd[key])
            pass
          pass
        pass

class AMQP_Client_Thread:
  __connection__: pika.BlockingConnection
  __clientChannel__: pika.adapters.blocking_connection.BlockingChannel
  def __init__(self, host, username, password, virtual_host: str = '/', port: int = 5672, heartbeat: int = 0):
    try:
      self.__connection__ = pika.BlockingConnection(
        pika.ConnectionParameters(
          host=host,
          port=port,
          virtual_host=virtual_host,
          heartbeat=heartbeat,
          credentials=pika.PlainCredentials(username, password)
        )
      )
    except pika.exceptions.AMQPConnectionError as e:
      raise e
  
  def create_RPC_Server(self, queue: str, on_message: None, prefetch_count: int):
    return RPC_Server_Thread(self.__connection__, queue, on_message, prefetch_count)
  def create_RPC_Client(self, queue: str, timeout: int = 0):
    if not hasattr(self, "__clientChannel__"):
      self.__clientChannel__ = self.__connection__.channel()
      self.__clientChannel__.confirm_delivery()
    return RPC_Client_Thread(self.__connection__, self.__clientChannel__, queue, timeout)

  def create_Queue_Server(self, queue: str, group: str, on_message: None, prefetch_count: int):
    return Queue_Server_Thread(self.__connection__, queue, group, on_message, prefetch_count)
  def create_Queue_Client(self, queue: str):
    if not hasattr(self, "__clientChannel__"):
      self.__clientChannel__ = self.__connection__.channel()
      self.__clientChannel__.confirm_delivery()
    return Queue_Client_Thread(self.__connection__, self.__clientChannel__, queue)

class RPC_Server:
  def __init__(self, id, queue, q: list):
    self.queue = queue
    self.id = id
    self.queueCmd = q
  def stop(self):
    self.queueCmd.append({
      "method": 'RPC_Server.stop',
      "args": {
        "id": self.id,
      }
    })

class RPC_Client:
  def __init__(self, id, queue, q: list, timeout: int):
    self.id = id
    self.queue = queue
    self.queueCmd = q
    self.timeout = timeout
  def send(self, routing_key: str, dataInput: dict):
    cmd = {
      "method": "RPC_Client.send",
      "args": {
        "routing_key": routing_key,
        "dataInput": dataInput,
        "id": self.id,
        "corr_id": str(uuid.uuid4()),
        "response": None,
        "exception": None
      }
    }
    self.queueCmd.append(cmd)
    period = 0.05
    t = 0
    while cmd['args']['response'] is None and cmd['args']['exception'] is None and (self.timeout == 0 or t < self.timeout):
      t += period
      time.sleep(period)
    if not (cmd['args']['exception'] is None):
      raise Exception(cmd['args']['exception'])
    if cmd['args']['response'] is None:
      raise Exception('REQUEST_WAS_TIMED_OUT')
    response: dict = cmd['args']['response']
    return response

class Queue_Server:
  def __init__(self, id, queue, q: list):
    self.queue = queue
    self.id = id
    self.queueCmd = q
  def stop(self):
    self.queueCmd.append({
      "method": 'Queue_Server.stop',
      "args": {
        "id": self.id,
      }
    })

class Queue_Client:
  def __init__(self, id, queue, q: list):
    self.id = id
    self.queue = queue
    self.queueCmd = q
  def send(self, routing_key: str, dataInput: dict):
    cmd = {
      "method": "Queue_Client.send",
      "args": {
        "routing_key": routing_key,
        "dataInput": dataInput,
        "id": self.id,
        "corr_id": str(uuid.uuid4()),
        "response": None,
        "exception": None
      }
    }
    self.queueCmd.append(cmd)
    period = 0.05
    while cmd['args']['response'] is None and cmd['args']['exception'] is None:
      time.sleep(period)
    if not (cmd['args']['exception'] is None):
      raise Exception(cmd['args']['exception'])
    if cmd['args']['response'] is None:
      raise Exception('REQUEST_WAS_TIMED_OUT')
    response: dict = cmd['args']['response']
    return response
