import asyncio
from urllib.parse import quote_plus
from classes.rabbitmq.classRabbitMqClient import MsRabbitMqClient
from config.config import settings
from pika.exchange_type import ExchangeType
from models.shared.modelEnvironment import MsEnvironment
from rabbitmq.MsRabbitMqConsts import RabbitMqRoutingKeyUserService

def CreateRabbitMqConnectionString() -> str:
    return f"amqp://{settings.rabbitmq.username}:{settings.rabbitmq.password}@{settings.rabbitmq.host}:{settings.rabbitmq.port}/{quote_plus(settings.rabbitmq.virtual_host)}"

rabbitMqClient = MsRabbitMqClient(
    amqp_url=CreateRabbitMqConnectionString(),
    prefetch_count=1,
    reconnect=True,
    reconnectDelaySec=settings.rabbitmq.reconnectDelaySec,
    ioloop=asyncio.get_running_loop(),
    allowPublishing=True,
    debug=settings.project.dev_mode,
    clientProduct=settings.project.serviceName + "-" + settings.project.environment.value,
    clientInformation=settings.project.environment.value
)

queueDefault  = rabbitMqClient.AddQueue(
    name=settings.rabbitmq.queueName,
    queueDurable=True if settings.project.environment != MsEnvironment.development else False,
    queueAutoDelete=True if settings.project.environment == MsEnvironment.development else False,
    consumerAllowConsuming=True
)

exchangeDefault = rabbitMqClient.AddExchange(
    exchangeName=settings.rabbitmq.exchangeName,
    exchangeType=ExchangeType.direct,
    exchangeDurable=True
)

for routingKey in RabbitMqRoutingKeyUserService:
    exchangeDefault.AddRoutingKey(
        routingKey=routingKey.value,
        queueName=queueDefault,
        consumerExclusive=False,
        consumerAllowConsuming=True
    )