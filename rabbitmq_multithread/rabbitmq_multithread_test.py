# 验证pika驱动rabbitmq的多线程应用
# 可在pika的BlockingConnection适配器下通过channel.consume迭代消费并配合add_callback_threadsafe来使用多线程
# add_callback_threadsafe是BlockingConnection唯一线程安全的方法
# 将迭代的消息交与主线程外的其他线程进行处理，并通过add_callback_threadsafe来添加一个消息确认
# 这样不会堵塞主线程对消息的消费
# 但是为了限制资源过度消耗，应该使用一个线程池例如ThreadPoolExcutor来执行消息
# 并通过设置prefech_count参数来防止执行主机的ThreadPollExcutor的队列消耗
# 照理是可以通过basic_get的while循环达到同样的效果
# 但是pika已经提供了consume迭代器，没必要在繁琐的使用basic_get了


import time
import pika
import random
from pika.adapters.blocking_connection import BlockingChannel
from pika import logging
from concurrent.futures import ThreadPoolExecutor
import functools


# 限定线程池中的线程数
# 同时同步设置rabbitmq的prefetch_count参数等同于线程数
SIZE = 32


class Publish:
    """
    发送测试消息
    """
    def __init__(self) -> None:
        self.__cerd = pika.PlainCredentials('test', 'test')
        self.__con_param = pika.ConnectionParameters("121.5.121.173", virtual_host="test", credentials=self.__cerd)
        self.connection = pika.BlockingConnection(self.__con_param)

    def __channel(self) -> BlockingChannel:
        return self.connection.channel()

    def declare_queue(self, channel: BlockingChannel, queue: str):
        channel.queue_declare(queue, durable=True)

    def publish_message(self):
        channel = self.__channel()
        self.declare_queue(channel, "test")

        for i in range(1000):
            channel.basic_publish(
                '',
                'test',
                f"hello world {i}",
            )

        logging.info(f"publish 100 message to queue named test")

    def __del__(self):
        self.connection.close()


class ThreadConsumer:
    """
    rabbitmq使用python多线程消费的实现
    """
    def __init__(self) -> None:
        self.__cerd = pika.PlainCredentials('test', 'test')
        self.__con_param = pika.ConnectionParameters("121.5.121.173", virtual_host="test", credentials=self.__cerd)
        self.connection = pika.BlockingConnection(self.__con_param)
        # 线程池提高性能
        self.tpool = ThreadPoolExecutor(SIZE)

    def __channel(self) -> BlockingChannel:
        return self.connection.channel()

    def declare_queue(self, channel: BlockingChannel, queue: str):
        channel.queue_declare(queue, durable=True)
        # 设置预取消息数量，避免线程池中的任务排队消费执行主机的内存
        channel.basic_qos(prefetch_count=SIZE)

    # 工作线程的主函数
    def __worker(self, channel: BlockingChannel, tag: int, body: bytes):
        # 模拟一个工作负载
        time.sleep(random.random()*2)
        print(body)
        # 添加消息确认，以便消息消费的继续
        # 从主线程外的线程添加
        self.connection.add_callback_threadsafe(
            functools.partial(channel.basic_ack, delivery_tag=tag)
        )

    def consume(self):
        channel = self.__channel()
        self.declare_queue(channel, "test")

        try:
            # 使用线程消费的迭代器模式
            # 可以转换为basic_get的while循环
            for method_fram, properties, body in channel.consume("test"):
                print(method_fram, properties, body)
                self.tpool.submit(self.__worker, channel, method_fram.delivery_tag, body)
        except KeyboardInterrupt:
            pass

    def __del__(self):
        # 在所有线程完成后在关闭rabbitmq的链接
        self.tpool.shutdown()
        self.connection.close()


if __name__ == "__main__":
    publish = Publish()
    publish.publish_message()
    consumer = ThreadConsumer()
    consumer.consume()