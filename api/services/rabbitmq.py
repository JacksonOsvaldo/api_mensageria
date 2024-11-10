from typing import Dict
import requests
from core.settings import RABBIT_MQ_HOST, RABBIT_MQ_PORT, RABBIT_MQ_USER, RABBIT_MQ_PASSWORD
import pika
import json


class RabbitmqService:
    """
    A class to interact with RabbitMQ server for creating exchanges, queues, and sending messages.
    """

    def __init__(self) -> None:
        """
        Initializes the RabbitmqService class, setting up the connection parameters and creating a channel.

        :raises pika.exceptions.AMQPConnectionError: If the connection to RabbitMQ fails.
        """
        self.__host = RABBIT_MQ_HOST
        self.__port = RABBIT_MQ_PORT
        self.__user = RABBIT_MQ_USER
        self.__password = RABBIT_MQ_PASSWORD
        self.__channel = self.__create_channel()

    def __create_channel(self):
        """
        Creates a new channel for communication with RabbitMQ.

        :return: The created channel for communication with RabbitMQ.
        :rtype: pika.BlockingChannel
        """
        connection_parameters = pika.ConnectionParameters(
            host=self.__host,
            port=self.__port,
            credentials=pika.PlainCredentials(
                username=self.__user,
                password=self.__password
            )
        )
        channel = pika.BlockingConnection(connection_parameters).channel()
        return channel

    def create_exchange(self, exchange_name: str) -> None:
        """
        Creates an exchange on the RabbitMQ server.

        :param exchange_name: The name of the exchange to be created.
        :type exchange_name: str
        :raises pika.exceptions.AMQPChannelError: If the channel creation fails.
        """
        self.__channel.exchange_declare(exchange=exchange_name, durable=True)

    def create_queue(self, queue_name: str) -> None:
        """
        Creates a queue on the RabbitMQ server.

        :param queue_name: The name of the queue to be created.
        :type queue_name: str
        :raises pika.exceptions.AMQPChannelError: If the queue creation fails.
        """
        self.__channel.queue_declare(queue=queue_name, durable=True)

    def queue_bind(
        self, exchange_name: str, queue_name: str, rout_key_name: str
    ) -> None:
        """
        Binds a queue to an exchange with a routing key.

        :param exchange_name: The name of the exchange to bind the queue to.
        :type exchange_name: str
        :param queue_name: The name of the queue to be bound.
        :type queue_name: str
        :param rout_key_name: The routing key used to bind the queue.
        :type rout_key_name: str
        :raises pika.exceptions.AMQPChannelError: If the binding fails.
        """
        self.__channel.queue_bind(
            exchange=exchange_name, queue=queue_name, routing_key=rout_key_name
        )

    def send_message(self, exchange_name: str, rout_key_name: str, body: Dict) -> None:
        """
        Sends a message to an exchange with a specific routing key.

        :param exchange_name: The name of the exchange where the message will be sent.
        :type exchange_name: str
        :param rout_key_name: The routing key used to route the message.
        :type rout_key_name: str
        :param body: The message body to be sent, which will be serialized to JSON.
        :type body: Dict
        :raises pika.exceptions.AMQPChannelError: If sending the message fails.
        """
        self.__channel.basic_publish(
            exchange=exchange_name,
            routing_key=rout_key_name,
            body=json.dumps(body),
            properties=pika.BasicProperties(delivery_mode=2),
        )

    def list_exchanges(self) -> list:
        """
        Retrieves the list of exchanges from the RabbitMQ server.

        :return: A list of exchanges on the RabbitMQ server.
        :rtype: list
        :raises Exception: If the request to retrieve exchanges fails.
        """
        url = f'http://{self.__host}:15672/api/exchanges'
        response = requests.get(url, auth=(self.__user, self.__password))

        if response.status_code == 200:
            exchanges = response.json()
            return exchanges
        else:
            raise Exception(f"Failed to retrieve exchanges: {response.status_code} - {response.text}")

    def list_queues(self) -> list:
        """
        Retrieves the list of queues from the RabbitMQ server.

        :return: A list of queues on the RabbitMQ server.
        :rtype: list
        :raises Exception: If the request to retrieve queues fails.
        """
        url = f'http://{self.__host}:15672/api/queues'
        response = requests.get(url, auth=(self.__user, self.__password))

        if response.status_code == 200:
            queues = response.json()
            return queues
        else:
            raise Exception(f"Failed to retrieve queues: {response.status_code} - {response.text}")
