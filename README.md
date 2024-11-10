# api_mensageria

API de agendamento de notificações usando serviço de mensageria.

### Instalação

Primeiro, faça o clone do projeto:

```bash
git clone git@github.com:JacksonOsvaldo/api_mensageria.git && cd api_mensageria
```

Agora, dentro da pasta do projeto, vamos subir nosso ambiente usando o [docker compose](https://docs.docker.com/compose/install/linux/):

```bash
docker compose up -d
```

Feito isso, nossos ambiente estarão onlines nas seguintes portas/rotas:

* **API: [http://localhost:8000](http://localhost:8000)**
  * Acessando a rota base do projeto, você será direcionado para a documentação da API;
  * Nesse ambiente, você consegue realizar todas as operações da API.
* **RabbitMQ: [http://localhost:15672](http://localhost:15672)**
  * Acessando essa rota, você será direcionado para a tela de login do ambiente;
  * No caso de ter mantido as configurações do docker-compose.yml, login e senha serão `guest`

### Testes

Antes de inciar os procedimentos na API, é recomendável realizar os testes:

```bash
docker exec django_api_mensageria python manage.py test tests
```

### Uso da aplicação

#### Configurando nossa fila

Nesse projeto, seguimos a linha de usar um exchange e ele fazer o gerenciamento da fila. Com isso, temos alguns passos iniciais.

- 1. Criar o exchange

```bash
curl --request POST \
  --url http://localhost:8000/api/v1/rabbitmq/create_exchange/ \
  --header 'Content-Type: application/json' \
  --data '{
  "exchange_name": "schedule_data"
}'
```

Nesse caso, estou criando uma com o nome `schedule_data`

- 2. Criar a fila

```bash
curl --request POST \
  --url http://localhost:8000/api/v1/rabbitmq/create_queue/ \
  --header 'Content-Type: application/json' \
  --data '{
  "queue_name": "schedule_queue"
}'
```

Nesse caso, estou criando uma com o nome `schedule_queue`

- 3. Fazer o bind da fila com o exchange

```bash
curl --request POST \
  --url http://localhost:8000/api/v1/rabbitmq/queue_bind/ \
  --header 'Content-Type: application/json' \
  --data '{
  "exchange_name": "schedule_data",
  "queue_name": "schedule_queue"
}'
```

Nesse caso, fizemos uma ligação entre a exchange `schedule_data` com a nossa queue `schedule_queue`

- 4. Adiconais
     Você pode, ainda, listar todas as exchanges:

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/api/v1/rabbitmq/list_exchanges/' \
  -H 'accept: application/json'
```

E pode listar, também, todas as queues:

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/api/v1/rabbitmq/list_queues/' \
  -H 'accept: application/json'
```

Um detalhe interessante é que você consegue fazer todas essas operações direto pela página de documentação da API.

#### Realizando as operações da API

Nossa API tem algumas rotas básicas, além das do RabbitMQ como serviço:

| Operação                            | Rota                                                      | Método |
| ------------------------------------- | --------------------------------------------------------- | ------- |
| Listar Status                         | http://127.0.0.1:8000/api/v1/schedules/get_status/           | GET     |
| Listar canais para agendamento        | http://127.0.0.1:8000/api/v1/schedules/get_channels/         | GET     |
| Criar Agendamento                     | http://127.0.0.1:8000/api/v1/schedules/create_schedule/      | POST    |
| Listar todos os agendamentos          | http://127.0.0.1:8000/api/v1/schedules/get_schedules/        | GET     |
| Cancelar um agendamento               | http://127.0.0.1:8000/api/v1/schedules/{id}/cancel/          | POST    |
| Checar status de agendamento por item | http://127.0.0.1:8000/api/v1/schedules/{id}/check/           | GET     |
| Atualizar parte de um item            | http://127.0.0.1:8000/api/v1/schedules/{id}/update_schedule/ | PUT     |

Para o caso de você desejar testar cada um isoladamente, recomendo começar pelos `status` e `channels`. Isso, porque você precisará do nome específico de cada um para realizar as operações de criação de agendamento e atualização de agendamento.

- 1. Listar Status 
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/api/v1/schedules/get_status/' \
  -H 'accept: application/json'
```

- 2. Listar Canais
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/api/v1/schedules/get_channels/' \
  -H 'accept: application/json'
```

- 3. Criar agendamento
No caso dessa rota, temos que passar o nome da exchange específica. Como criamos a `schedule_data` mais cedo, usaremos ela.

```bash
curl --request POST \
  --url http://localhost:8000/api/v1/schedules/create_schedule/\
  --header 'Content-Type: application/json' \
  --data '{
	"recipient": "55919854504",
	"message": "Sua compra foi confirmada!",
	"scheduled_datetime": "2024-12-01T10:00:00Z",
	"channel": "whatsapp",
	"exchange": "schedule_data"
}'
```

- 4. Listar todos os agendamentos
```bash
curl --request GET \
  --url http://127.0.0.1:8000/api/v1/schedules/get_schedules/
```

- 5. Cancelando Agendamento
Nesse caso, precisamos passar o ID do item que queremos cancelar. Levando em consideração que queremos cancelar o item com o ID 1, seguimos assim:
```bash
curl --request POST \
  --url http://127.0.0.1:8000/api/v1/schedules/1/cancel/
```

- 6. Checar status de agendamento
Aqui, também precisamos passar o ID do item que queremos checar. Levando em consideração que queremos checar o item com o ID 1, seguimos assim:
```bash
curl --request GET \
  --url http://127.0.0.1:8000/api/v1/schedules/1/check/
```

- 7. Atualizar parte de um item
Aqui, também precisamos passar o ID do item que queremos alterar. Levando em consideração que queremos alterar o item com o ID 1, seguimos assim:
```bash
curl --request PUT \
  --url http://127.0.0.1:8000/api/v1/schedules/1/update_schedule/ \
  --header 'Content-Type: application/json' \
  --data '{
	"recipient": "email-novo@example.com",
	"message": "Mensagem nova",
	"channel": "email"
}'
```

Nesse caso, estamos alterando o `recipient`, a `message` e o `channel`.