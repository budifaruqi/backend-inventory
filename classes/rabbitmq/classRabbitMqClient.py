import asyncio
from datetime import datetime
from enum import Enum
import functools
from asyncio import AbstractEventLoop, Task
import json
import threading
from time import sleep
from typing import Any, Awaitable, Callable
from fastapi.encoders import jsonable_encoder
from pika import URLParameters
from pika.exceptions import AMQPError, ChannelClosedByBroker, AMQPChannelError, ConnectionClosed, ConnectionClosedByClient, ConnectionClosedByBroker
from pika.spec import Basic, BasicProperties, Queue, Exchange
from pika.frame import Method
from pika.adapters.asyncio_connection import AsyncioConnection
from pika.channel import Channel
from pika.exchange_type import ExchangeType
from classes.rabbitmq.classRabbitMqUtils import (
    MsRabbitMqChannelNotLoaded,
    MsRabbitMqDisconnecting,
    MsRabbitMqException,
    MsRabbitMqExchangeAlreadyExists,
    MsRabbitMqExchangeNotFound,
    MsRabbitMqNotActive,
    MsRabbitMqQueueNotFound
)
from models.shared.modelDataType import BaseModel
from utils.util_logger import msLogger

class MsRabbitMqPublishResponse:
    def __init__(
        self,
        err: MsRabbitMqException | AMQPError | Exception | None,
        exchange: str,
        routingKey: str,
        body: str | bytes,
        properties: BasicProperties
    ) -> None:
        self.err = err
        self.exchange = exchange
        self.routingKey = routingKey
        self.body = body
        self.properties = properties
    

class MsRabbitMqHandlerResult(int, Enum):
    ack = 1
    nack = -1

MsRabbitMqHandler = Callable[
    [
        'MsRabbitMqQueue',
        Basic.Deliver,      # method
        BasicProperties,    # properties
        bytes               # body
    ],
    Awaitable[MsRabbitMqHandlerResult]
]

class MsRabbitMqConfigHandler:
    def __init__(
        self,
        queue: 'MsRabbitMqQueue',
        routingKey: str | None,
        handler: MsRabbitMqHandler
    ) -> None:
        self.queue = queue
        self.routingKey = routingKey
        self.handler = handler

def rabbitmq_run_in_event_loop(func: Callable[..., Any]):
    @functools.wraps(func)
    def wrapper(self: 'MsRabbitMqClient', *args: Any, **kwargs: Any):
        wrapped = functools.partial(func, self, *args, **kwargs)
        self.ioloop.call_soon_threadsafe(wrapped)
    return wrapper

class MsRabbitMqQueueBind:

    def __init__(
        self,
        exchange: 'MsRabbitMqExchange',
        routingKey: 'MsRabbitMqRoutingKey | None',
        queue: 'MsRabbitMqQueue'
    ) -> None:
        self.exchange = exchange
        self.routingKey = routingKey
        self.queue = queue
        self.loading_ = False
        self.loaded_ = False

    def start_(self):
        self.loading_ = False
        self.loaded_ = False

class MsRabbitMqQueue:
    def __init__(
        self,
        owner: 'MsRabbitMqClient',
        name: str,
        *,
        shutdown_timeout_seconds: int = 20,

        queuePassive: bool = False,
        queueDurable: bool = False,
        queueExclusive: bool = False,
        queueAutoDelete: bool = False,
        queueArguments: dict[str, Any] | None = None,
        
        consumerTag: str | None = None,
        consumerAutoAck: bool = False,
        consumerExclusive: bool = False,
        consumerArguments: dict[str, Any] | None = None,
        consumerAllowConsuming: bool = True
    ) -> None:
        self.owner = owner
        self.name = name
        """
        Queue name
        """

        self.queuePassive = queuePassive
        self.queueDurable = queueDurable
        self.queueExclusive = queueExclusive
        self.queueAutoDelete = queueAutoDelete
        self.queueArguments = queueArguments

        self.consumerTag = consumerTag
        self.consumerAutoAck = consumerAutoAck
        self.consumerExclusive = consumerExclusive
        self.consumerArguments = consumerArguments
        self.consumerAllowConsuming = consumerAllowConsuming

        self.bindingList_: list[MsRabbitMqQueueBind] = []
        self._pending_futures: set[Task[None]] = set()
        self._shutdown_timeout_seconds = shutdown_timeout_seconds

        self.loading_ = False
        self.loaded_ = False
        self.queueName_: str | None = None
        self.consumer_auto_ack_ = False
        self.consumer_tag_: str | None = None
        self.stop_consuming_ = False
        self.consuming_ = False
        self.was_consuming_ = False
        self.stoping_ = False
        
        self._name = self.__class__.__name__
        self.owner.queueList_.append(self)
        self.update_name_()
        msLogger.success(f"{self}")

    def update_name_(self):
        ret = f"<rabbit_consumer::queue::{self.name}"
        if self.consumer_tag_ is not None:
            ret += f"::{self.consumer_tag_}"
        self._name = ret

    def __repr__(self) -> str:
        return self._name

    def start_(self):
        self._pending_futures.clear()
        self.loading_ = False
        self.loaded_ = False
        self.queueName_ = None
        self.consumer_auto_ack_ = False
        self.consumer_tag_ = None
        self.stop_consuming_ = False
        self.consuming_ = False
        self.was_consuming_ = False
        self.stoping_ = False

        for binding in self.bindingList_:
            binding.start_()
            
        self.update_name_()

    def shutdown(self):
        while len(self._pending_futures) > 0:
            try:
                f = self._pending_futures.pop()
                if not f.done():
                    self.stoping_ = True
                    tStart = datetime.now().timestamp()
                    waitSeconds = self._shutdown_timeout_seconds
                    while (not f.done()):
                        sleep(0.1)
                        # wait for waitSeconds seconds
                        if datetime.now().timestamp() - tStart > waitSeconds:
                            # force shutdown
                            msLogger.warning(f"{self} is timeout ({waitSeconds}) seconds")
                            break
                    if not f.done():
                        f.cancel()
            except Exception as e:
                msLogger.warning(f"{self}::shutdown; error; {str(e)}")

        self._pending_futures.clear()

    def addBinding(self, exchange: 'MsRabbitMqExchange', routingKey: 'MsRabbitMqRoutingKey | None'):
        for binding in self.bindingList_:
            if (binding.exchange == exchange) and (binding.routingKey == routingKey):
                return binding
        ret = MsRabbitMqQueueBind(exchange, routingKey, self)
        self.bindingList_.append(ret)
        return ret
    
    def bindWithExchange(self, exchange: 'MsRabbitMqExchange'):
        for binding in self.bindingList_:
            if (binding.exchange == exchange) and (binding.routingKey == None):
                return binding
        ret = MsRabbitMqQueueBind(exchange, None, self)
        self.bindingList_.append(ret)
        return ret

    def _on_message_callback(self, channel: Channel, method: Basic.Deliver, properties: BasicProperties, body: bytes):
        if (not self.consuming_) or (self.stoping_):
            return
        def donecb(f: Task[None]):
            self._pending_futures.discard(f)
            try:
                f.result()
            except Exception as err:
                msLogger.critical(str(err), err, False)

        coro = self.do_on_message(channel, method, properties, body)
        t = self.owner.ioloop.create_task(coro)
        t.add_done_callback(donecb)
        self._pending_futures.add(t)
        # f.result()
        # coro = MsRabbitMqConsumerQueue.do_on_message()
        # future = asyncio.run_coroutine_threadsafe(coro, self.owner._ioloop)
        # future.result()
            
        # asyncio.e
        # self.owner._ioloop.run_until_complete(MsRabbitMqConsumerQueue.do_on_message(self))
        # channel.basic_ack(method.delivery_tag)

    async def do_on_message(self, channel: Channel, method: Basic.Deliver, properties: BasicProperties, body: bytes):
        msLogger.success(f"do_on_message; threadId: {threading.get_native_id()}")
        handled = False
        ret = MsRabbitMqHandlerResult.ack
        for handler in self.owner.handlers_:
            if handler.queue != self:
                continue
            if handler.routingKey is not None:
                if handler.routingKey != method.routing_key:
                    continue
            handled = True
            try:
                ret = await handler.handler(self, method, properties, body)
            except Exception as errHandler:
                ret = MsRabbitMqHandlerResult.ack
                msLogger.error(f"Error executting callback rabbitmq consumer; method: {method}; properties: {properties}; {str(errHandler)}")
            break
        if (self.owner.debug_) and (not handled):
            msLogger.data(f"Unhandled callback; method: {method}; properties: {properties}")

        if not self.consumer_auto_ack_:
            if ret == MsRabbitMqHandlerResult.ack:
                channel.basic_ack(method.delivery_tag)
            else:
                channel.basic_nack(method.delivery_tag)

class MsRabbitMqRoutingKey:
    def __init__(
        self,
        owner: 'MsRabbitMqClient',
        name: str,
        queue: MsRabbitMqQueue,
        exchange: 'MsRabbitMqExchange'
    ) -> None:
        self.owner = owner
        self.name = name.strip()
        self.queue = queue
        self.exchange = exchange
        self.loaded_ = False

        self.exchange.routingKeyList.append(self)
        self.queue.addBinding(self.exchange, self)

class MsRabbitMqExchange:
    def __init__(
        self,
        owner: 'MsRabbitMqClient',
        name: str,
        type: ExchangeType,
        *,
        passive: bool = False,
        durable: bool = False,
        auto_delete: bool = False,
        internal: bool = False,
        arguments: dict[str, Any] | None = None
    ) -> None:
        name = name.strip()
        exchangeNameLower = name.lower()
        
        for exchange in owner.exchangeList_:
            if exchange.name.lower() == exchangeNameLower:
                raise MsRabbitMqExchangeAlreadyExists(name)
        
        self.owner = owner
        self.name = name
        self.type = type
        self.passive = passive
        self.durable = durable
        self.auto_delete = auto_delete
        self.internal = internal
        self.arguments = arguments
        self.loading_ = False
        self.loaded_ = False
        self.routingKeyList: list[MsRabbitMqRoutingKey] = []

        self.owner.exchangeList_.append(self)

    def AddRoutingKey(
        self,
        routingKey: str,
        queueName: str | MsRabbitMqQueue,
        *,

        queuePassive: bool = False, # Ignored if `queueName` is `MsRabbitMqConsumerQueue`
        queueDurable: bool = False, # Ignored if `queueName` is `MsRabbitMqConsumerQueue`
        queueExclusive: bool = False, # Ignored if `queueName` is `MsRabbitMqConsumerQueue`
        queueAutoDelete: bool = False, # Ignored if `queueName` is `MsRabbitMqConsumerQueue`
        queueArguments: dict[str, Any] | None = None, # Ignored if `queueName` is `MsRabbitMqConsumerQueue`

        consumerTag: str | None = None,
        consumerAutoAck: bool = False, # Ignored if `queueName` is `MsRabbitMqConsumerQueue`
        consumerExclusive: bool = False, # Ignored if `queueName` is `MsRabbitMqConsumerQueue`
        consumerArguments: dict[str, Any] | None = None, # Ignored if `queueName` is `MsRabbitMqConsumerQueue`
        consumerAllowConsuming: bool = True # Ignored if `queueName` is `MsRabbitMqConsumerQueue`
    ) -> MsRabbitMqRoutingKey:
        routingKey = routingKey.strip()
        queue: MsRabbitMqQueue | None = None

        if isinstance(queueName, str):
            queueName = queueName.strip()
            
            if not consumerExclusive:
                for nRoutingKey in self.routingKeyList:
                    if nRoutingKey.name == routingKey:
                        return nRoutingKey
            
            queue = self.owner.AddQueue(
                queueName,

                queuePassive=queuePassive,
                queueDurable=queueDurable,
                queueExclusive=queueExclusive,
                queueAutoDelete=queueAutoDelete,
                queueArguments=queueArguments,
                
                consumerTag=consumerTag,
                consumerAutoAck=consumerAutoAck,
                consumerExclusive=consumerExclusive,
                consumerArguments=consumerArguments,
                consumerAllowConsuming=consumerAllowConsuming
            )
        else:
            for q in self.owner.queueList_:
                if q == queueName:
                    queue = q
                    break
            if queue is None:
                raise MsRabbitMqQueueNotFound(queueName.name if queueName.name != "" else None)

        return MsRabbitMqRoutingKey(
            self.owner,
            name=routingKey,
            queue=queue,
            exchange=self
        )

    def start_(self):
        self.loading_ = False
        self.loaded_ = False
        for routingKey in self.routingKeyList:
            routingKey.loaded_ = False

class MsRabbitMqClient:

    def __init__(
        self,
        amqp_url: str,
        *,
        prefetch_count: int = 0,
        reconnect: bool = True,
        reconnectDelaySec: int = 10,
        ioloop: AbstractEventLoop | None = None,
        allowPublishing: bool = False,
        debug: bool = False,
        clientProduct: str | None = None,
        clientInformation: str | None = None
    ):
        self.clientProduct = clientProduct
        self.clientInformation = clientInformation
        self._connection: AsyncioConnection | None = None
        self._closing = False

        self._url = amqp_url
        self.ioloop = ioloop or asyncio.get_running_loop()

        self._reconnect = reconnect
        if reconnectDelaySec < 0:
            reconnectDelaySec = 1
        self._reconnectDelaySec = reconnectDelaySec
        self.debug_ = debug
        if prefetch_count < 0:
            prefetch_count = 0
        self._prefetch_count = prefetch_count
        self._allowPublishing = allowPublishing
        self.channel_: Channel | None = None
        self._active = False
        self.exchangeList_: list[MsRabbitMqExchange] = []
        self.queueList_: list[MsRabbitMqQueue] = []
        self._isReady = False
        self._requestShutdown = False
        self._auto_reconnect_timer = None
        self._pending_auto_reconnect: set[Task[None]] = set()
        self._reconnect_started = False
        self.handlers_: list[MsRabbitMqConfigHandler] = []
        self._recover = True

    @property
    def ExchangeList(self) -> list[MsRabbitMqExchange]:
        return self.exchangeList_

    def RegisterHandler(
        self,
        queue: MsRabbitMqQueue,
        routingKey: str | None = None
    ):

        def func(handler: MsRabbitMqHandler) -> MsRabbitMqHandler:
            self.handlers_.append(MsRabbitMqConfigHandler(queue=queue, routingKey=routingKey, handler=handler))
            return handler
        return func
    
    def AddQueue(
        self,
        name: str,
        *,
        shutdown_timeout_seconds: int = 20,

        queuePassive: bool = False,
        queueDurable: bool = False,
        queueExclusive: bool = False,
        queueAutoDelete: bool = False,
        queueArguments: dict[str, Any] | None = None,

        consumerTag: str | None = None,
        consumerAutoAck: bool = False,
        consumerExclusive: bool = False,
        consumerArguments: dict[str, Any] | None = None,
        consumerAllowConsuming: bool = True
    ) -> MsRabbitMqQueue:
        queueName = name.strip()
        if not consumerExclusive:
            for nQueue in self.queueList_:
                if nQueue.consumerAutoAck:
                    continue
                if nQueue.name == queueName:
                    return nQueue
            
        return MsRabbitMqQueue(
            self,
            queueName,
            shutdown_timeout_seconds=shutdown_timeout_seconds,

            queuePassive=queuePassive,
            queueDurable=queueDurable,
            queueExclusive=queueExclusive,
            queueAutoDelete=queueAutoDelete,
            queueArguments=queueArguments,
            
            consumerTag=consumerTag,
            consumerAutoAck=consumerAutoAck,
            consumerExclusive=consumerExclusive,
            consumerArguments=consumerArguments,
            consumerAllowConsuming=consumerAllowConsuming
        )
    
    def AddExchange(
        self,
        exchangeName: str,
        exchangeType: str | ExchangeType,
        *,
        exchangePassive: bool = False,
        exchangeDurable: bool = False,
        exchangeAutoDelete: bool = False,
        exchangeInternal: bool = False,
        exchangeArguments: dict[str, Any] | None = None
    ):
        exchangeName = exchangeName.strip()
        
        exchangeNameLower = exchangeName.lower()
        
        for exchange in self.exchangeList_:
            if exchange.name.lower() == exchangeNameLower:
                return exchange
        if isinstance(exchangeType, str):
            exchangeType = ExchangeType[exchangeType]
        return MsRabbitMqExchange(
            self,
            exchangeName,
            exchangeType,
            passive=exchangePassive,
            durable=exchangeDurable,
            auto_delete=exchangeAutoDelete,
            internal=exchangeInternal,
            arguments=exchangeArguments
        )

    def AddPipeline(
        self,
        exchangeName: str,
        exchangeType: str | ExchangeType,
        routingKey: str,
        queueName: str,
        *,
        exchangePassive: bool = False,
        exchangeDurable: bool = False,
        exchangeAutoDelete: bool = False,
        exchangeInternal: bool = False,
        exchangeArguments: dict[str, Any] | None = None,

        queuePassive: bool = False,
        queueDurable: bool = False,
        queueExclusive: bool = False,
        queueAutoDelete: bool = False,
        queueArguments: dict[str, Any] | None = None,

        consumerTag: str | None = None,
        consumerAutoAck: bool = False,
        consumerExclusive: bool = False,
        consumerAllowConsuming: bool = True
    ) -> MsRabbitMqExchange:
        selExchange = self.AddExchange(
            exchangeName=exchangeName,
            exchangeType=exchangeType,
            exchangePassive=exchangePassive,
            exchangeDurable=exchangeDurable,
            exchangeAutoDelete=exchangeAutoDelete,
            exchangeInternal=exchangeInternal,
            exchangeArguments=exchangeArguments
        )

        selExchange.AddRoutingKey(
            routingKey,
            queueName,

            queuePassive=queuePassive,
            queueDurable=queueDurable,
            queueExclusive=queueExclusive,
            queueAutoDelete=queueAutoDelete,
            queueArguments=queueArguments,

            consumerTag=consumerTag,
            consumerAutoAck=consumerAutoAck,
            consumerExclusive=consumerExclusive,
            consumerAllowConsuming=consumerAllowConsuming
        )

        return selExchange
        
    def start(self):
        if self._active:
            return
        self._isReady = False
        self._active = True
        self._recover = True
        for exchange in self.exchangeList_:
            exchange.start_()
        for queue in self.queueList_:
            queue.start_()
        self._do_connect()

    async def Shutdown(self):
        self._requestShutdown = True
        try:
            while len(self._pending_auto_reconnect) > 0:
                f = self._pending_auto_reconnect.pop()
                if not f.done():
                    f.cancel()

        except:
            pass
        self._pending_auto_reconnect.clear()
        self._stop_timer_reconnect()
        self._stop()

    def _stop(self):
        if not self._closing:
            if self._closing:
                raise MsRabbitMqDisconnecting()
            self._recover = False
            self._closing = True
            self._isReady = False
            if self.debug_:
                msLogger.info(f"{__name__}::stop::Stopping")
            self._do_stop()
            if self.debug_:
                msLogger.info(f"{__name__}::stop::Stopped")

    def _do_connect(self):
        if self.debug_:
            msLogger.info(f'{__name__}::do_connect; {self._url}')
        productName = "MsRabbitMqClient"
        if self.clientProduct:
            productName += "-" + self.clientProduct
        client_properties: dict[str, Any] = {
            "product": productName
        }
        if self.clientInformation:
            client_properties["information"] = self.clientInformation
        parameters = URLParameters(self._url)
        parameters.client_properties = client_properties
        return AsyncioConnection(
            parameters=parameters,
            on_open_callback=self._connection_on_open,
            on_open_error_callback=self._connection_on_open_error, # type: ignore
            on_close_callback=self._connection_on_closed, # type: ignore
            custom_ioloop=self.ioloop
        )
    
    def _connection_on_open_error(
        self,
        conn: AsyncioConnection,
        err: AMQPError
    ):
        if self.debug_:
            msLogger.error(f"{__name__}::connection_on_open_error::{type(err)}; {str(err)}")
        else:
            msLogger.warning("Failed to open connection")
        if self._reconnect and (not self._requestShutdown):
            self._do_reconnect()

    def _connection_on_closed(self, conn: AsyncioConnection, reason: AMQPError):
        self.channel_ = None
        self._connection = None
        self._closing = False
        self._active = False
        if isinstance(reason, ConnectionClosedByBroker):
            msLogger.success(f"{__name__}::connection_on_closed; ConnectionClosedByBroker; status: {reason.reply_code}; reason: {str(reason.reply_text)}") # type: ignore
        elif isinstance(reason, ConnectionClosedByClient):
            self._recover = False
            if self.debug_:
                msLogger.error(f"{__name__}::connection_on_closed; ConnectionClosedByClient; status: {reason.reply_code}; reason: {str(reason.reply_text)}") # type: ignore
        elif isinstance(reason, ConnectionClosed):
            msLogger.error(f"{__name__}::connection_on_closed; ConnectionClosed; status: {reason.reply_code}; reason: {str(reason.reply_text)}") # type: ignore
        if (self._recover):
            if self.debug_:
                msLogger.warning(f"{__name__}::connection_on_closed; reconnect necessary: {reason} {type(reason)}")
            if self._reconnect:
                self._do_reconnect()

    def _connection_on_open(self, conn: AsyncioConnection):
        if self.debug_:
            msLogger.success(f"{__name__}::connection_on_open; Connection opened")
        self._connection = conn
        
        self._connection.channel(on_open_callback=self._channel_on_open)

    def _do_reconnect(self):
        if self.debug_:
            msLogger.warning(f"{__name__}::do_reconnect; preparing")
        self.should_reconnect = True
        self._stop()
        if self.debug_:
            msLogger.warning(f"{__name__}::do_reconnect; reconnecting ...", foreground="cyan")
            self._start_reconnect()
        
    def _do_stop(self):
        if self._active:
            self._do_stop_consuming()
        else:
            self._closing = False
            self._active = False

    def _do_stop_consuming(self):
        """Tell RabbitMQ that you would like to stop consuming by sending the
        Basic.Cancel RPC command.

        """
        for queue in self.queueList_:
            queue.stoping_ = True
        for queue in self.queueList_:
            queue.shutdown()
        _stopConsumer = False
        if (self.channel_ is not None):
            for queue in self.queueList_:
                if (queue.consumerAllowConsuming) and (queue.consuming_) and (queue.was_consuming_) and (queue.consumer_tag_ is not None) and (not queue.stop_consuming_):
                    msLogger.info('Sending a Basic.Cancel RPC command to RabbitMQ')
                    cb = functools.partial(
                        self._on_cancelok, # type: ignore
                        queue=queue
                    )
                    queue.stop_consuming_ = True
                    self.channel_.basic_cancel(queue.consumer_tag_, cb)
                    _stopConsumer = True

        if not _stopConsumer:
            self._close_channel()

    def _on_cancelok(
        self,
        frame: Method, # type: ignore
        queue: MsRabbitMqQueue
    ):
        if self.debug_:
            msLogger.info(f'RabbitMQ acknowledged the cancellation of the consumer queue: {queue}::{queue.consumer_tag_}')

        queue.consuming_ = False
        queue.was_consuming_ = False
        queue.consumer_tag_ = None

        # wait all queue stop consuming
        for queue in self.queueList_:
            if not queue.consumerAllowConsuming:
                continue
            if queue.was_consuming_:
                return
            
        self._close_channel()

    def _close_channel(self):
    
        """Call to close the channel with RabbitMQ cleanly by issuing the
        Channel.Close RPC command.

        """
        if self.debug_:
            msLogger.info(f"{__name__}::close_channel; Closing the channel")
        if self.channel_ is not None:
            self.channel_.close()
        elif self._connection is not None:
            if (not self._connection.is_closing) or (not self._connection.is_closed):
                self._connection.close()
        else:
            self._closing = False
            self._active = False

    def _channel_on_close(self, channel: Channel, reason: AMQPError):
        self._closing = True
        if self.debug_:
            if isinstance(reason, ChannelClosedByBroker):
                msLogger.error(f"{__name__}::channel_on_close; Channel closed; channel_number: {channel.channel_number}; status: {reason.reply_code}; reason: {str(reason.reply_text)}") # type: ignore
            else:
                msLogger.error(f"{__name__}::channel_on_close; {type(reason)} {reason}")
        self.channel_ = None
        if isinstance(reason, AMQPChannelError):
            self._recover = False
        if self._connection is not None:
            if (not self._connection.is_closing) or (not self._connection.is_closed):
                try:
                    self._connection.close()
                except Exception as e:
                    msLogger.error(f"{__name__}::channel_on_close; Error closing connection; {e}")
        else:
            self._closing = False
            self._active = False

    def _channel_on_open(self, channel: Channel):
        self.channel_ = channel
        self.channel_.add_on_close_callback(self._channel_on_close) # type: ignore

        if self.debug_:
            msLogger.success(f"{__name__}::channel_on_open; Loading exchanges")

        hasExchange = False
        for exchange in self.exchangeList_:
            hasExchange = True
            if (exchange.loading_) or (exchange.loaded_):
                continue
            exchange.loading_ = True
            cbExchange = functools.partial(
                self._exchange_on_declareok, # type: ignore
                exchange=exchange
            )
            self.channel_.exchange_declare(
                exchange=exchange.name,
                exchange_type=exchange.type,
                passive=exchange.passive,
                durable=exchange.durable,
                auto_delete=exchange.auto_delete,
                internal=exchange.internal,
                arguments=exchange.arguments,
                callback=cbExchange
            )

        if not hasExchange:
            self._setup_queue()

    def _exchange_on_declareok(self, frame: Method, exchange: MsRabbitMqExchange): # type: ignore
        if not isinstance(frame.method, Exchange.DeclareOk): # type: ignore
            return
        if self.debug_:
            msLogger.success(f"{__name__}::exchange_on_declareok; Exchange declared {exchange.name}")
        if self.channel_ is None:
            return
        exchange.loaded_ = True

        # wait all exchange loaded
        for exchange in self.exchangeList_:
            if (not exchange.loading_) or (not exchange.loaded_):
                return
            
        self._setup_queue()
        
    def _setup_queue(self):
        if self.channel_ is None:
            return
        if self.debug_:
            msLogger.info(f"{__name__}::setup_queue; Loading queues")

        hasQueue = False
        # load queue
        for queue in self.queueList_:
            hasQueue = True
            if (queue.loading_) or (queue.loaded_):
                continue

            queue.loading_ = True
            cbQueue = functools.partial(
                self._queue_on_declareok, # type: ignore
                queue=queue
            )
            self.channel_.queue_declare(
                queue=queue.name,
                passive=queue.queuePassive,
                durable=queue.queueDurable,
                exclusive=queue.queueExclusive,
                auto_delete=queue.queueAutoDelete,
                arguments=queue.queueArguments,
                callback=cbQueue
            )

        if not hasQueue:
            if self.debug_:
                msLogger.info(f"{__name__}::setup_queue; Empty queue")
            self._setup_publisher_and_consumer()

    def _queue_on_declareok(self, frame: Method, queue: MsRabbitMqQueue): # type: ignore
        if not isinstance(frame.method, Queue.DeclareOk): # type: ignore
            return
        queue.queueName_ = frame.method.queue
        queue.loaded_ = True
        # _unused_frame.queue
        if self.channel_ is None:
            return
        if self.debug_:
            msLogger.info("queue loaded " + queue.queueName_)

        # wait all queue loaded
        for q in self.queueList_:
            if (not q.loading_) or (not q.loaded_):
                return
            
        hasBinding = False
        # queue bind
        for q in self.queueList_:
            if len(q.bindingList_) == 0:
                continue
            hasBinding = True
            for queueBinding in q.bindingList_:
                if queueBinding.loading_ or queueBinding.loaded_:
                    continue
                queueBinding.loading_ = True
                cbQueueBind = functools.partial(
                    self._queue_bind_on_ok, # type: ignore
                    queueBinding=queueBinding
                )
                self.channel_.queue_bind(
                    queue=queueBinding.queue.queueName_ if queueBinding.queue.queueName_ is not None else queueBinding.queue.name,
                    exchange=queueBinding.exchange.name,
                    routing_key=queueBinding.routingKey.name if queueBinding.routingKey is not None else None,
                    callback=cbQueueBind
                )
        if not hasBinding:
            self._setup_publisher_and_consumer()
    
    def _queue_bind_on_ok(self, frame: Method, queueBinding: MsRabbitMqQueueBind): # type: ignore
        if not isinstance(frame.method, Queue.BindOk): # type: ignore
            return
        queueBinding.loaded_ = True
        if queueBinding.routingKey is not None:
            queueBinding.routingKey.loaded_ = True
        if self.channel_ is None:
            return
        # print("_queue_bind_on_ok; frame", frame)
        if self.debug_:
            s = queueBinding.exchange.name
            if queueBinding.routingKey is not None:
                s += "-" + queueBinding.routingKey.name
            s += "-" + queueBinding.queue.queueName_ if queueBinding.queue.queueName_ is not None else queueBinding.queue.name
            msLogger.info("queueBinding loaded " + s)

        # wait all queueBinding loaded
        for queue in self.queueList_:
            if not queue.loaded_:
                return
            if len(queue.bindingList_) == 0:
                continue
            for queueBinding in queue.bindingList_:
                if (not queueBinding.loading_) or (not queueBinding.loaded_):
                    return
                
        self._setup_publisher_and_consumer()
                
    def _setup_publisher_and_consumer(self):
        if self.channel_ is None:
            return

        hasConsumer = False
        for queue in self.queueList_:
            if queue.consumerAllowConsuming:
                hasConsumer = True
                break

        if self._allowPublishing:
            if self.debug_:
                msLogger.info(f"{__name__}::setup_publisher_and_consumer; Setup confirm_delivery")
            self.channel_.confirm_delivery(
                self._on_delivery_confirmation # type: ignore
            )

        if hasConsumer:
            if self.debug_:
                msLogger.info(f"{__name__}::setup_publisher_and_consumer; Configuring basic QOS; prefetch_count: {self._prefetch_count}")
            self.channel_.basic_qos(
                prefetch_count=self._prefetch_count,
                callback=self._basic_qos_on_ok # type: ignore
            )
        else:
            self._isReady = True
            if self.debug_:
                msLogger.success(f"{__name__}::setup_publisher_and_consumer; Client ready", foreground="red")
    
    def _consumer_on_cancelled(self, frame: Method): # type: ignore
        if self.channel_:
            self.channel_.close()
    
    def _basic_qos_on_ok(self, frame: Method): # type: ignore
        # print("_basic_qos_on_ok; frame", frame)
        if not isinstance(frame.method, Basic.QosOk): # type: ignore
            return
        if self.channel_ is None:
            return
        if self.debug_:
            msLogger.info(f"{__name__}::basic_qos_on_ok; QOS loaded")
        self.channel_.add_on_cancel_callback(self._consumer_on_cancelled) # type: ignore

        for queue in self.queueList_:
            if not queue.consumerAllowConsuming:
                continue
            if queue.consuming_:
                continue
            queue.consuming_ = True
            cbQueueBind = functools.partial(
                self._queue_consumeOk, # type: ignore
                queue=queue
            )
            queue.consumer_auto_ack_ = queue.consumerAutoAck
            if self.debug_:
                msLogger.info(f"{__name__}::basic_qos_on_ok; Consuming; Queue: '{queue.name}'; auto_ack: {queue.consumer_auto_ack_}; tag: {queue.consumerTag if queue.consumerTag is not None else 'null'}")

            self.channel_.basic_consume(
                queue=queue.name,
                on_message_callback=queue._on_message_callback, # type: ignore
                auto_ack=queue.consumer_auto_ack_,
                exclusive=queue.consumerExclusive,
                consumer_tag=queue.consumerTag,
                arguments=queue.consumerArguments,
                callback=cbQueueBind
            )

    def _queue_consumeOk(self, frame: Method, queue: MsRabbitMqQueue): # type: ignore
        if not isinstance(frame.method, Basic.ConsumeOk): # type: ignore
            return
        queue.consumer_tag_ = frame.method.consumer_tag
        queue.was_consuming_ = True
        queue.update_name_()
        if self.debug_:
            msLogger.success(f"{__name__}::queue_consumeOk; Queue name: '{queue.name}' tag: '{queue.consumer_tag_}'")

        for queue in self.queueList_:
            if not queue.consumerAllowConsuming:
                continue
            if (not queue.consuming_) or (not queue.was_consuming_):
                return
            
        self._isReady = True
        if self.debug_:
            msLogger.success(f"{__name__}::queue_consumeOk; Client ready", foreground="red")

    def _on_delivery_confirmation(self, frame: Method): # type: ignore
        if not isinstance(frame.method, Basic.Ack): # type: ignore
            return
        # print(type(frame.method))
        confirmation_type = frame.method.NAME.split('.')[1].lower()
        ack_multiple = frame.method.multiple
        delivery_tag = frame.method.delivery_tag

        msLogger.info(f"Received '{confirmation_type}' for delivery tag: '{delivery_tag}' (multiple: {ack_multiple})")

    async def _do_publish(
        self,
        exchange: str,
        routingKey: str,
        body: str | bytes,
        properties: BasicProperties | None = None
    ) -> MsRabbitMqPublishResponse:
        if not self._active:
            return MsRabbitMqPublishResponse(
                MsRabbitMqNotActive(),
                exchange,
                routingKey,
                body,
                properties if properties else BasicProperties()
            )
        if self.channel_ is None:
            return MsRabbitMqPublishResponse(
                MsRabbitMqChannelNotLoaded(),
                exchange,
                routingKey,
                body,
                properties if properties else BasicProperties()
            )
        try:
            self.channel_.basic_publish(
                exchange,
                routingKey,
                body=body,
                properties=properties
            )
        except Exception as err:
            if self.debug_:
                msLogger.error(f"{__name__}::__do_publish; {str(err)}")
            return MsRabbitMqPublishResponse(
                err,
                exchange,
                routingKey,
                body,
                properties if properties else BasicProperties()
            )
        
        return MsRabbitMqPublishResponse(
            None,
            exchange,
            routingKey,
            body,
            properties if properties else BasicProperties()
        )

    async def _do_publish_string(
        self,
        exchange: str,
        routingKey: str,
        body: str,
        properties: BasicProperties | None = None
    ) -> MsRabbitMqPublishResponse:
        data = body.encode(encoding="utf-8")
        if not properties:
            properties = BasicProperties(
                content_type="text/plain"
            )
        else:
            properties.content_type = "text/plain"
        return await self._do_publish(exchange, routingKey, data, properties)

    async def _do_publish_dictionary(
        self,
        exchange: str,
        routingKey: str,
        body: dict[str, Any],
        properties: BasicProperties | None = None
    ) -> MsRabbitMqPublishResponse:
        data = json.dumps(
            jsonable_encoder(body),
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":")
        ).encode(encoding="utf-8")
        if not properties:
            properties = BasicProperties(
                content_type="application/json"
            )
        else:
            properties.content_type = "application/json"
        return await self._do_publish(exchange, routingKey, data, properties)

    async def _do_publish_model(
        self,
        exchange: str,
        routingKey: str,
        body: BaseModel,
        properties: BasicProperties | None = None,
        by_alias: bool = True
    ) -> MsRabbitMqPublishResponse:
        data = body.model_dump(
            mode="json",
            by_alias=by_alias
        )
        return await self._do_publish_dictionary(exchange, routingKey, data, properties)

    def _ValidateSource(
        self,
        exchangeName: str | MsRabbitMqExchange
    ) -> MsRabbitMqExchange | str:
        selExchange: MsRabbitMqExchange | str | None = None
        if isinstance(exchangeName, str):
            for exchange in self.exchangeList_:
                if exchange.name == exchangeName:
                    selExchange = exchange
                    break
            if not selExchange:
                if (exchangeName == "") or (exchangeName.startswith("amq.")):
                    selExchange = exchangeName
                else:
                    raise MsRabbitMqExchangeNotFound(exchangeName)
        else:
            if exchangeName not in self.exchangeList_:
                raise MsRabbitMqExchangeNotFound(exchangeName.name)
            selExchange = exchangeName
        
        return selExchange
    
    async def publish(
        self,
        exchangeName: str | MsRabbitMqExchange,
        routingKeyName: str,
        body: str | bytes,
        properties: BasicProperties | None = None
    ) -> MsRabbitMqPublishResponse:
        selExchange = self._ValidateSource(
            exchangeName=exchangeName
        )
        
        return await self._do_publish(
            selExchange.name if isinstance(selExchange, MsRabbitMqExchange) else selExchange,
            routingKeyName,
            body,
            properties
        )

    async def publish_string(
        self,
        exchangeName: str | MsRabbitMqExchange,
        routingKeyName: str,
        body: str,
        properties: BasicProperties | None = None
    ) -> MsRabbitMqPublishResponse:
        selExchange = self._ValidateSource(
            exchangeName=exchangeName
        )
        
        return await self._do_publish_string(
            selExchange.name if isinstance(selExchange, MsRabbitMqExchange) else selExchange,
            routingKeyName,
            body,
            properties
        )

    async def publish_dictionary(
        self,
        exchangeName: str | MsRabbitMqExchange,
        routingKeyName: str,
        body: dict[str, Any],
        properties: BasicProperties | None = None
    ) -> MsRabbitMqPublishResponse:
        selExchange = self._ValidateSource(
            exchangeName=exchangeName
        )
        
        return await self._do_publish_dictionary(
            selExchange.name if isinstance(selExchange, MsRabbitMqExchange) else selExchange,
            routingKeyName,
            body,
            properties
        )

    async def publish_model(
        self,
        exchangeName: str | MsRabbitMqExchange,
        routingKeyName: str,
        body: BaseModel,
        properties: BasicProperties | None = None,
        by_alias: bool = False
    ) -> MsRabbitMqPublishResponse:
        selExchange = self._ValidateSource(
            exchangeName=exchangeName
        )
        
        return await self._do_publish_model(
            selExchange.name if isinstance(selExchange, MsRabbitMqExchange) else selExchange,
            routingKeyName,
            body,
            properties,
            by_alias
        )

    def _start_reconnect(self):
        self._stop_timer_reconnect()
        self._start_timer_reconnect()

    def _start_timer_reconnect(self):
        self._stop_timer_reconnect()
        self._auto_reconnect_timer = self.ioloop.call_later(self._reconnectDelaySec, self._reconnect_proc, self)

    def _stop_timer_reconnect(self):
        if self._auto_reconnect_timer:
            self._auto_reconnect_timer.cancel()
            del self._auto_reconnect_timer
            self._auto_reconnect_timer = None

    @rabbitmq_run_in_event_loop
    def _reconnect_proc(self, _):
        def callback(f: Task[None]):
            self._pending_auto_reconnect.discard(f)
            try:
                f.result()
            except BaseException as err:
                self._reconnect_started = False
                msLogger.error(f"Failed to execute reconnect. {str(err)}", err, False)
            else:
                self._reconnect_started = False

        if (not self._reconnect_started) and (self._reconnect) and (not self._requestShutdown):
            self._reconnect_started = True
            coro = self._begin_reconnect()
            f = self.ioloop.create_task(coro)
            f.add_done_callback(callback)
            self._pending_auto_reconnect.add(f)

    async def _begin_reconnect(self):
        msLogger.success("Reconnecting ...")
        if self._requestShutdown:
            return
        self.start()