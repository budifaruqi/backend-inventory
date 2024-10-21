import json
from pika.spec import Basic, BasicProperties
from config.config import settings
from classes.rabbitmq.classRabbitMqClient import MsRabbitMqHandlerResult, MsRabbitMqQueue
from models.account.modelAccountConsume import AccountConsume
from models.account_external.modelAccountExternalConsume import AccountExternalConsume
from models.company.modelCompanyConsume import CompanyConsume
from models.company_category.modelCompanyCategoryConsume import CompanyCategoryConsume
from models.shared.modelEnvironment import MsEnvironment
from rabbitmq.MsRabbitMq import rabbitMqClient, queueDefault
from rabbitmq.MsRabbitMqConsts import RabbitMqRoutingKeyUserService
from repositories.repoAccount import AccountRepository
from repositories.repoAccountExternal import AccountExternalRepository
from repositories.repoCompany import CompanyRepository
from repositories.repoCompanyCategory import CompanyCategoryRepository
from utils.util_logger import msLogger


@rabbitMqClient.RegisterHandler(queueDefault, RabbitMqRoutingKeyUserService.company_category)
async def consumer_user_service_company_category(
    queue: MsRabbitMqQueue,
    method: Basic.Deliver,
    properties: BasicProperties,
    body: bytes
) -> MsRabbitMqHandlerResult:
    routingKey = str(method.routing_key)
    if settings.project.environment == MsEnvironment.development:
        msLogger.data(f"Consumer::{queue.name}::{routingKey};\n"
            f"method: {method}\n"
            f"properties: {properties}\n"
            f"body: {json.dumps(json.loads(body), indent=2)}"
        )
    try:
        dataJson = json.loads(body)
    except Exception as jsonError:
        msLogger.exception(f"Consumer::{queue.name}::{routingKey}::Invalid_Json\n", jsonError, False)
        return MsRabbitMqHandlerResult.ack
    
    try:
        data = CompanyCategoryConsume(**dataJson)
    except Exception as modelError:
        msLogger.exception(f"Consumer::{queue.name}::{routingKey}::CompanyCategoryConsume\n", modelError, False)
        return MsRabbitMqHandlerResult.ack
    
    await CompanyCategoryRepository.CreateOrUpdate(
        data.id,
        data
    )
    return MsRabbitMqHandlerResult.ack

@rabbitMqClient.RegisterHandler(queueDefault, RabbitMqRoutingKeyUserService.company)
async def consumer_user_service_company(
    queue: MsRabbitMqQueue,
    method: Basic.Deliver,
    properties: BasicProperties,
    body: bytes
) -> MsRabbitMqHandlerResult:
    routingKey = str(method.routing_key)
    if settings.project.environment == MsEnvironment.development:
        msLogger.data(f"Consumer::{queue.name}::{routingKey};\n"
            f"method: {method}\n"
            f"properties: {properties}\n"
            f"body: {json.dumps(json.loads(body), indent=2)}"
        )
    try:
        dataJson = json.loads(body)
    except Exception as jsonError:
        msLogger.exception(f"Consumer::{queue.name}::{routingKey}::Invalid_Json\n", jsonError, False)
        return MsRabbitMqHandlerResult.ack
    
    try:
        data = CompanyConsume(**dataJson)
    except Exception as modelError:
        msLogger.exception(f"Consumer::{queue.name}::{routingKey}::CompanyConsume\n", modelError, False)
        return MsRabbitMqHandlerResult.ack
    
    await CompanyRepository.CreateOrUpdate(
        data.id,
        data
    )
    return MsRabbitMqHandlerResult.ack

@rabbitMqClient.RegisterHandler(queueDefault, RabbitMqRoutingKeyUserService.account)
async def consumer_user_service_account(
    queue: MsRabbitMqQueue,
    method: Basic.Deliver,
    properties: BasicProperties,
    body: bytes
) -> MsRabbitMqHandlerResult:
    routingKey = str(method.routing_key)
    if settings.project.environment == MsEnvironment.development:
        msLogger.data(f"Consumer::{queue.name}::{routingKey};\n"
            f"method: {method}\n"
            f"properties: {properties}\n"
            f"body: {json.dumps(json.loads(body), indent=2)}"
        )
    try:
        dataJson = json.loads(body)
    except Exception as jsonError:
        msLogger.exception(f"Consumer::{queue.name}::{routingKey}::Invalid_Json\n", jsonError, False)
        return MsRabbitMqHandlerResult.ack
    
    try:
        data = AccountConsume(**dataJson)
    except Exception as modelError:
        msLogger.exception(f"Consumer::{queue.name}::{routingKey}::AccountConsume\n", modelError, False)
        return MsRabbitMqHandlerResult.ack
    
    await AccountRepository.CreateOrUpdate(
        data.id,
        data
    )
    return MsRabbitMqHandlerResult.ack

@rabbitMqClient.RegisterHandler(queueDefault, RabbitMqRoutingKeyUserService.account_external)
async def consumer_user_service_account_external(
    queue: MsRabbitMqQueue,
    method: Basic.Deliver,
    properties: BasicProperties,
    body: bytes
) -> MsRabbitMqHandlerResult:
    routingKey = str(method.routing_key)
    if settings.project.environment == MsEnvironment.development:
        msLogger.data(f"Consumer::{queue.name}::{routingKey};\n"
            f"method: {method}\n"
            f"properties: {properties}\n"
            f"body: {json.dumps(json.loads(body), indent=2)}"
        )
    try:
        dataJson = json.loads(body)
    except Exception as jsonError:
        msLogger.exception(f"Consumer::{queue.name}::{routingKey}::Invalid_Json\n", jsonError, False)
        return MsRabbitMqHandlerResult.ack
    
    try:
        data = AccountExternalConsume(**dataJson)
    except Exception as modelError:
        msLogger.exception(f"Consumer::{queue.name}::{routingKey}::AccountExternalConsume\n", modelError, False)
        return MsRabbitMqHandlerResult.ack
    
    await AccountExternalRepository.CreateOrUpdate(
        data.id,
        data
    )
    return MsRabbitMqHandlerResult.ack

