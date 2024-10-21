class MsRabbitMqException(Exception):
    def __repr__(self) -> str:
        return "An unspecified error"
    def __str__(self) -> str:
        return self.__repr__()
    
class MsRabbitMqExchangeAlreadyExists(MsRabbitMqException):
    def __init__(self, exchangeName: str) -> None:
        self.exchangeName = exchangeName

    def __repr__(self):
        return f"Exchange '{self.exchangeName}' already exists"
    def __str__(self) -> str:
        return self.__repr__()
    
class MsRabbitMqExchangeNotFound(MsRabbitMqException):
    def __init__(self, exchangeName: str | None = None) -> None:
        self.exchangeName = exchangeName

    def __repr__(self):
        return "Exchange not found" + f" {self.exchangeName}" if self.exchangeName is not None else ""
    def __str__(self) -> str:
        return self.__repr__()

class MsRabbitMqRoutingKeyNotFound(MsRabbitMqException):
    def __init__(self, routingKeyName: str | None = None) -> None:
        self.routingKeyName = routingKeyName

    def __repr__(self):
        s = "Routing key not found"
        if self.routingKeyName is not None:
            s += f" '{self.routingKeyName}'"
        return s
    def __str__(self) -> str:
        return self.__repr__()

class MsRabbitMqRoutingKeyNotLoaded(MsRabbitMqException):
    def __init__(self, routingKeyName: str | None = None, exchangeName: str | None = None) -> None:
        self.routingKeyName = routingKeyName
        self.exchangeName = exchangeName

    def __repr__(self):
        s = "Routing key not loaded"
        if (self.routingKeyName is not None) and (self.routingKeyName != ""):
            s += f" '{self.routingKeyName}'"
        if (self.exchangeName is not None) and (self.exchangeName != ""):
            s += f" '{self.exchangeName}'"
        return s
    def __str__(self) -> str:
        return self.__repr__()
    
class MsRabbitMqRoutingKeyPublishingNotAllowed(MsRabbitMqException):
    def __init__(self, routingKeyName: str | None = None, exchangeName: str | None = None) -> None:
        self.routingKeyName = routingKeyName
        self.exchangeName = exchangeName

    def __repr__(self):
        s = "Publishing throught this routing key not allowed"
        if (self.routingKeyName is not None) and (self.routingKeyName != ""):
            s += f" '{self.routingKeyName}'"
        if (self.exchangeName is not None) and (self.exchangeName != ""):
            s += f" '{self.exchangeName}'"
        return s
    def __str__(self) -> str:
        return self.__repr__()
    
class MsRabbitMqQueueNotFound(MsRabbitMqException):
    def __init__(self, queueName: str | None = None) -> None:
        self.queueName = queueName

    def __repr__(self):
        s = "Queue name not found"
        if self.queueName is not None:
            s += f" '{self.queueName}'"
        return s
    def __str__(self) -> str:
        return self.__repr__()
    
class MsRabbitMqChannelNotLoaded(MsRabbitMqException):
    def __repr__(self):
        return "Channel not loaded"
    def __str__(self) -> str:
        return self.__repr__()
    
class MsRabbitMqNotActive(MsRabbitMqException):
    def __repr__(self):
        return "Client not active"
    def __str__(self) -> str:
        return self.__repr__()
    
class MsRabbitMqDisconnecting(MsRabbitMqException):
    def __repr__(self):
        return "Client in  disconnecting state"
    def __str__(self) -> str:
        return self.__repr__()
    