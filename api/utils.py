import pika
import json
from core.settings import RABBIT_MQ


class RabbitMQConector:

    @staticmethod
    def get_rabbitmq_connection():
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_MQ))
        return connection
    
    def send_to_queue(self, queue_name, message):
        connection = self.get_rabbitmq_connection()
        channel = connection.channel()
        channel.queue_declare(queue=queue_name, durable=True)
        channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,
            )
        )
        connection.close()

    def check_message_status_in_queue(self, queue_name, message_id):
        connection = self.get_rabbitmq_connection()
        channel = connection.channel()

        # Consumir a mensagem da fila e verificar se o ID corresponde
        method_frame, header_frame, body = channel.basic_get(queue=queue_name, auto_ack=False)

        while method_frame:
            message = json.loads(body)
            
            # Verificar se a mensagem corresponde ao message_id fornecido
            if message.get('id') == message_id:
                # Confirma e remove a mensagem da fila
                channel.basic_ack(delivery_tag=method_frame.delivery_tag)
                connection.close()
                return True  # Retorna True se a mensagem foi encontrada e removida
            
            # Caso não tenha sido a mensagem correta, continue consumindo
            method_frame, header_frame, body = channel.basic_get(queue=queue_name, auto_ack=False)

        connection.close()
        return False


