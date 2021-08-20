# -*- coding: utf-8 -*-


"""
    此模块包含两个队列类，分别用于分布式的RabbitMQ和用于本地运行的Queue。
"""


import pika
import pickle
import time
from pika import BasicProperties
from pika.exceptions import AMQPChannelError, ChannelClosed, ConnectionClosedByBroker, ChannelClosedByBroker, AMQPConnectionError, ConnectionClosed
from pika.exchange_type import ExchangeType


class RabbitMQ:
    """
    该类中大部分方法只是pika的简单包装，可以通过channel方法获取channel后使用pika的原生操作。
    此队列使用了阻塞链接，非线程安全类型，每个实例都将创建一个链接和一个通道。且没有提供常规队列的get，而是通过一个迭代器来消费队列。
    通过publish来发布消息到队列。队列中的消息是pickle打包的二进制字节对象。
    建议使用方法是在主线程获取消息，但是为了不阻塞住线程，将消息处理传给其他线程，并通过add_callback_threadsafe安全添加消息的交付确认：
        def ack(conn, channel, method, body):
            process(body)
            conn.add_callback_threadsafe(
                functools.partial(
                    channel.basic_ack, method.delivery_tag
                )
            )
        for method, properties, body in channel().consume():
            Thread(target=ack, args=(conn, channel, method, body)).start()
    """
    def __init__(self, username="guest", password="guest", *, host="127.0.0.1", port=5672, vhost="/") -> None:
        """
        本类型只提供了RabbitMQ的最基本的自定义参数，其余参数都使用了其默认值。
        """
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.__cred = pika.PlainCredentials(username, password)
        self.__con_params = pika.ConnectionParameters(host, port, virtual_host=vhost, credentials=self.__cred)
        self.__connection = None
        self.__channel = None
        self.__connecting = False  # 是否有链接正在进行的指示
        self.__channeling = False  # 是否有通道创建的动作指示

    def connect(self, retry_delay=3):
        """
        链接rabbitmq服务器，只有在初次链接或链接关闭且没有其他链接尝试的情况下执行，保证实例只有一个链接。
        除非为主动退出关闭或者服务器主动拒绝，否则一直重试，直到成功。
        :params:
        :retry_delay: 链接失败后重试的事件间隔，秒
        """
        if (self.__connection is None or self.__connection.is_closed) and not self.__connecting:
            self.__connecting = True
            while self.__connecting:
                try:
                    self.__connection = pika.BlockingConnection(self.__con_params)
                    self.__connecting = False
                except (KeyboardInterrupt, ConnectionClosedByBroker):
                    self.__connecting = False
                except (ConnectionClosed, AMQPConnectionError) as e:
                    time.sleep(retry_delay)
                    continue
        return self.__connection

    def channel(self, retry_delay=3):
        """
        创建通道，只有在初次创建或管道关闭且没有其他管道尝试的情况下执行。
        除非为主动退出关闭或者服务器主动拒绝，否则一直重试，直到成功。
        :params:
        :retry_delay: 创建失败后重试的事件间隔，秒
        """
        if (self.__channel is None or self.__channel.is_closed) and not self.__channeling:
            self.__channeling = True
            while self.__channeling:
                try:
                    self.__channel = self.__connection.channel()
                    self.__channeling = False
                except (KeyboardInterrupt, ChannelClosedByBroker):
                    self.__channeling = False
                except (ChannelClosed, AMQPChannelError) as e:
                    time.sleep(retry_delay)
                    continue
        return self.__channel

    def add_callback_threadsafe(self, callback):
        """
        该方法是唯一一个线程安全的方法，用于其他线程一个函数安全调用。
        :params:
        :callback: 回调函数，需要functools.partial()包装。
        """
        self.__connection.add_callback_threadsafe(callback)

    def declare_exchange(self, exname, extype=ExchangeType.direct, durable=False):
        """
        创建一个名为exname的direct类型的交换机，只有特定需要时才需要创建，
        否则使用默认交换机。返回spec.Exchange.DeclareOk。
        """
        # 默认交换机即为无名direct交换机
        # 每个队列都会默认绑定默认交换机
        if exname == "":
            return
        return self.__channel.exchange_declare(exname, exchange_type=extype, durable=durable)

    def declare_queue(self, qname, *, exname="", routing_key=None, durable=False):
        """
        队列声明，创建不存在的指定名称队列，可以是空字符串，此时队列名称为服务器创建。
        返回值为rabbitmq的spec.Queue.DeclareOk，包含队列名称。
        队列绑定，绑定到交换机和路由键。返回rabbitmq的spec.Queue.BindOk。
        :params:
        :qname: 队列名，str；
        :qname: 队列名，str；
        :exname: 交换机名，str；
        :routing_key: 路由键，str，默认None；
        :durable: 队列持久化，bool，默认False；
        """
        queue_name = self.__channel.queue_declare(qname, durable=durable).method.queue
        if exname != "":
            self.__channel.queue_bind(queue_name, exname, routing_key)
        return queue_name

    def basic_qos(self, prefetch_count=0):
        """
        本rabbitmq消息队列不允许设置no-ack，所有的消息都需要ack确认。
        当prefetch_count=0时，所有消息可以不用等待ack而被消费者获取，
        当prefetch_count>0时，消费者只能获取不大于prefetch_count的
        为ack的消息，此参数可以配合线程池使用。
        :params:
        :prefetch_count: int，预取消息数量，且暂时没有ack。
        """
        self.__channel.basic_qos(prefetch_count=prefetch_count)

    def consume(self, qname, auto_ack=False):
        """
        开始消费队列，返回的是一个迭代器，迭代器将阻塞当前链接和所在线程。
        可以通过channel.cancel()主动取消或者由服务器终结。
        迭代内容是一个三元组。：
        tuple(spec.Basic.Deliver, spec.BasicProperties, str or unicode)
        :params:
        :qname: 队列名，str；
        :auto_ack: 是否自动确认交付，bool，默认为Fasle。
        """
        return self.__channel.consume(qname, auto_ack=auto_ack)

    def basic_ack(self, delivery_tag):
        """
        主动确认交付。当consume的auto_ack参数为False时必须主动确认交付。
        :params:
        :delivery_tag: 服务器为每一条消息分配的唯一交付标签，可由spec.Basic.Delever.delivery_tag获得
        """
        self.__channel.basic_ack(delivery_tag=delivery_tag)

    def basic_nack(self, delivery_tag, requeue=True):
        """
        主动取消交付。默认将重入队，交付给其他消费者。
        :params:
        :delivery_tag: 服务器为每一条消息分配的唯一交付标签，可由spec.Basic.Delever.delivery_tag获得
        :require: 消息是否重新入队，bool，True则交与其他消费者，否则将被丢弃或成为死信。
        """
        self.__channel.basic_nack(delivery_tag=delivery_tag, requeue=requeue)

    def publish(self, body, routing_key, *, exname="", properties=BasicProperties(delivery_mode=2)):
        """
        发布消息到指定队列。默认使用默认交换机并进行消息持久化。
        :params:
        :body: 消息主题一般为字节串
        :routing_key: 队列路由，直连交换机为队列名称
        :exname: 交换机名称，默认使用默认交换机
        :properties: 消息属性，是BasicPorperties实例，默认进行消息持久化
        """
        self.__channel.basic_publish(
            exchange=exname,
            routing_key=routing_key,
            body=pickle.dumps(body),
            properties=properties
        )

    def get(self, qname):
        """
        单词获取单条队列中的消息。返回值为：
        (spec.Basic.GetOk|None, spec.BasicProperties|None, str|None)
        当队列为空时，方法会立即返回一个元素为None的三元组。
        :params:
        :qname: 队列名称，str
        """
        return self.__channel.basic_get(qname)