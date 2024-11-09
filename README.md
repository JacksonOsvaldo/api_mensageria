# api_mensageria

API de agendamento de notificações usando serviço de mensageria.


**POST /schedules/** para criar um novo agendamento e enviá-lo para a fila.

**GET /schedules/{id}/check/** para checar o status do agendamento.

**POST /schedules/{id}/cancel/** para cancelar um agendamento.

**PUT /schedules/{id}/update_schedule/** para atualizar um agendamento.
