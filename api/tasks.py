from celery import shared_task
from .models import CommunicationSchedule, Status
import time

@shared_task
def send_communication(schedule_id):
    """
    Tarefa que simula o envio de uma comunicação e atualiza o status
    tanto no banco de dados quanto na fila RabbitMQ.
    """
    schedule = CommunicationSchedule.objects.get(id=schedule_id)
    
    # Simula o tempo de envio
    time.sleep(5)
    
    # Atualiza o status para 'sent' no banco
    sent_status = Status.objects.get(name='sent')
    schedule.status = sent_status
    schedule.save()
    
    # Log para simulação
    print(f"Message sent to {schedule.recipient} via {schedule.channel.name}")
    
    # Envia uma confirmação para a fila RabbitMQ
    # rabbitmq_send_status(schedule_id, 'sent')  # Função fictícia para exemplo
