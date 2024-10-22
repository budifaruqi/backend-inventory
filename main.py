from contextlib import asynccontextmanager
from datetime import datetime, timezone
from http import HTTPStatus
import json
import os
from typing import Any, Callable, Coroutine
from pymongo.errors import PyMongoError, OperationFailure, ServerSelectionTimeoutError
from fastapi import Body, FastAPI, Request, Response
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from elasticapm.contrib.starlette import make_apm_client, ElasticAPM # type: ignore
from pydantic import ValidationError
from classes.classOpenApiNo422 import OpenApiNo422
from config.config import settings
from models.shared.modelEnvironment import MsEnvironment
from models.shared.modelResponse import SuccessMessage
from mongodb.mongoClient import MGDB
from rabbitmq.MsRabbitMq import rabbitMqClient
from utils.util_fastapi_trustedhost import MsTrustedHostMiddleware
from utils.util_file import FileUtil
from utils.util_http_exception import MsHTTPException
from utils.util_http_response import MsHTTPExceptionMessage, MsHTTPExceptionType, MsHTTPStatusCode
from utils.util_logger import msLogger
from utils.util_other import OtherUtil
from utils.validation_error.MsValidationError import FastApiParseError

rootPath = settings.fastapi.root_path
appDesc = settings.fastapi.description

docs_path: str | None = None
openapi_path: str | None = None
redoc_path: str | None = None

git_log_filename = "./git_log.txt"
if os.path.exists(git_log_filename):
    try:
        with open(git_log_filename) as git_log_f:
            git_log_str = git_log_f.read()
            git_log_arr = git_log_str.split(";")
            appDesc += "<br />" + "<br />".join(f'`{w}`' for w in git_log_arr)
    except:
        # ignore any exception
        pass
    
if settings.fastapi.openapi_path is not None:
    openapi_path = rootPath + settings.fastapi.openapi_path

    if settings.fastapi.docs_path is not None:
        docs_path = rootPath + settings.fastapi.docs_path

    if settings.fastapi.redoc_path is not None:
        redoc_path = rootPath + settings.fastapi.redoc_path

        appDesc += f"""
            <br />
            <a href="{redoc_path}" target="_blank" title="API Doc">API Doc</a>
            """
    
@asynccontextmanager
async def AppLifeSpan(app: FastAPI):
    msLogger.info("Starting " + settings.fastapi.project_name, foreground="yellow")

    # remove open api 422
    OpenApiNo422(app)

    if not FileUtil.CreateDirectory("./temp"):
        raise Exception(f"Failed to create directory temp")

    rabbitMqClient.start()

    msLogger.success("*** " + settings.fastapi.project_name + " Started ***", foreground="green")

    yield
    
    msLogger.warning("Stopping " + settings.fastapi.project_name)

    await rabbitMqClient.Shutdown()

    msLogger.success(f"*** {settings.fastapi.project_name} Stopped ***", foreground="red")

async def default_not_found(request: Request, exc: Any) -> Response:
    if isinstance(exc, MsHTTPException):
        return JSONResponse(
            content={
                "detail": exc.Json()
            },
            status_code=exc.status_code,
            headers=exc.headers
        )
    else:
        headers = getattr(exc, "headers", None)
        return JSONResponse(
            content=jsonable_encoder(
                {
                    "detail": {
                        "status_code": 404,
                        "error": HTTPStatus.NOT_FOUND.phrase.upper(),
                        "type": MsHTTPExceptionType.PAGE_NOT_FOUND.value,
                        "message": MsHTTPExceptionMessage.PAGE_NOT_FOUND.value,
                        "timestamp": datetime.now(timezone.utc).replace(microsecond=0)
                    }
                }
            ),
            status_code=404,
            headers=headers
        )

app = FastAPI(
    title=settings.fastapi.project_name,
    openapi_url=openapi_path,
    docs_url=docs_path,
    description=appDesc,
    version=settings.fastapi.version,
    debug=settings.fastapi.debug,
    swagger_ui_parameters={
        "syntaxHighlight.activate": True,
        "syntaxHighlight.theme": "arta",
        "docExpansion": "none",
        "filter": True,
        "tryItOutEnabled": False,
        "deepLinking": True,
        "displayRequestDuration": True,
        "displayOperationId": True,
        "showExtensions": True,
        "showCommonExtensions": True
    },
    redoc_url=redoc_path,
    lifespan=AppLifeSpan,
    exception_handlers={
        404: default_not_found
    },
    openapi_tags=[
        {
            "name": "Master Data Management",
            "description": "Perusahaan"
        },{
            "name": "Master Data Follower Management",
            "description": "Perusahaan"
        },
    ]
)

apmClient = None
if settings.project.environment != MsEnvironment.development:
    if (settings.apm.prefix is not None) and (settings.apm.server is not None):
        # apm service name = prefix-service_name-environment
        apmServiceName = str(settings.apm.prefix + "-" + settings.project.serviceName + "-" + settings.project.environment.value).replace(" ", "-").lower()
        # apm environment = prefix-environment
        apmEnvironment = str(settings.apm.prefix + "-" + settings.project.environment.value).lower()
        apmClient = make_apm_client(
            {
                "SERVICE_NAME": apmServiceName,
                "ENVIRONMENT": apmEnvironment,
                "SERVER_URL": settings.apm.server,
                "TRANSACTION_IGNORE_URLS": ["/health"],
                "DISABLE_METRICS": "*.cpu.*,system.memory.total,system.process.memory.*",
            }
        )

@app.middleware("http")
async def http_middleware_handler(request: Request, call_next: Callable[..., Any]):
    try:
        response = await call_next(request)
        return response
    except Exception as err:
        if apmClient is not None:
            try:
                apmClient.capture_exception() # type: ignore
            except:
                pass
        
        if isinstance(err, ResponseValidationError):
            respStatusCode = MsHTTPStatusCode.RESPONSE_VALIDATION_ERROR.value
            respName = MsHTTPStatusCode.RESPONSE_VALIDATION_ERROR.name
            respPhrase = MsHTTPStatusCode.RESPONSE_VALIDATION_ERROR.phrase
        elif isinstance(err, ValidationError):
            respStatusCode = MsHTTPStatusCode.VALIDATION_ERROR.value
            respName = MsHTTPStatusCode.VALIDATION_ERROR.name
            respPhrase = MsHTTPStatusCode.VALIDATION_ERROR.phrase
        elif isinstance(err, ServerSelectionTimeoutError):
            respStatusCode = MsHTTPStatusCode.DATABASE_CONNECTION_TIMEOUT.value
            respName = MsHTTPStatusCode.DATABASE_CONNECTION_TIMEOUT.name
            respPhrase = MsHTTPStatusCode.DATABASE_CONNECTION_TIMEOUT.phrase
        elif isinstance(err, OperationFailure):
            respStatusCode = MsHTTPStatusCode.OPERATION_DATABASE_ERROR.value
            respName = MsHTTPStatusCode.OPERATION_DATABASE_ERROR.name
            respPhrase = MsHTTPStatusCode.OPERATION_DATABASE_ERROR.phrase
        elif isinstance(err, PyMongoError):
            respStatusCode = MsHTTPStatusCode.DATABASE_ERROR.value
            respName = MsHTTPStatusCode.DATABASE_ERROR.name
            respPhrase = MsHTTPStatusCode.DATABASE_ERROR.phrase
        else:
            respStatusCode = HTTPStatus.INTERNAL_SERVER_ERROR.value
            respName = HTTPStatus.INTERNAL_SERVER_ERROR.name
            respPhrase = HTTPStatus.INTERNAL_SERVER_ERROR.phrase

        try:
            if isinstance(err, ValidationError):
                valError = err.errors(include_url=False)
                if settings.project.dev_mode:
                    for errorItem in valError:
                        for eItem, errorObj in errorItem.items():
                            if eItem == "input":
                                if (isinstance(errorObj, Coroutine)) or (isinstance(errorObj, Callable)):
                                    valError = err.errors(include_url=False, include_input=False)
                                    respStatusCode = MsHTTPStatusCode.VALIDATION_ERROR_INPUT_IS_COROUTINE.value
                                    respName = MsHTTPStatusCode.VALIDATION_ERROR_INPUT_IS_COROUTINE.name
                                    respPhrase = MsHTTPStatusCode.VALIDATION_ERROR_INPUT_IS_COROUTINE.phrase
                                break
                    if len(valError) > 0:
                        sError = valError[0].get("msg")
                    else:
                        sError = "Terjadi kesalahan internal validasi data"
                    displayError = sError
                else:
                    sError = "Terjadi kesalahan validasi data"
                    displayError = sError
            elif isinstance(err, ServerSelectionTimeoutError):
                sError = "Koneksi kedatabase timeout"
                displayError = sError
            elif isinstance(err, OperationFailure):
                sError = "Operasi database error"
                if settings.project.dev_mode:
                    displayError = sError
                else:
                    displayError = "Terjadi kesalahan pada perintah query database"
            elif isinstance(err, PyMongoError):
                sError = "Database error"
                displayError = sError
            else:
                sError = str(err)
                if settings.project.dev_mode:
                    displayError = sError
                else:
                    displayError = "Terjadi kesalahan sistem"
        except Exception as eGetError:
            msLogger.critical(f"eGetError: {str(eGetError)}")
            # sometimes we got unprintable error, like unsupported response model
            sError = "Unprintable error."
            if isinstance(err, ValidationError):
                sError += " Detail: Validation error."
            displayError = sError
                
        if (sError == ""):
            if isinstance(err, ResponseValidationError):
                sError = "Unsupported response"
                displayError = sError
                
        errorDetail: dict[str, Any] = {
            "status_code": respStatusCode,
            "error": respName,
            "type": respPhrase,
            "message": displayError,
            "timestamp": datetime.now(timezone.utc).replace(microsecond=0),
            "method": request.method,
            "path": request.url.path,
            "query_params": request.query_params
        }
        if settings.project.dev_mode:
            errorDetail["exceptionType"] = str(type(err))
            if isinstance(err, OperationFailure):
                try:
                    errorDetail["extendedMessage"] = err.details
                except:
                    errorDetail["extendedMessage"] = str(err)
            elif isinstance(err, ServerSelectionTimeoutError):
                try:
                    errorDetail["extendedMessage"] = str(err)
                except:
                    pass
            elif isinstance(err, PyMongoError):
                errorDetail["extendedMessage"] = str(err)
            elif isinstance(err, ResponseValidationError):
                errorDetail["responseBody"] = err.body

            msLogger.exception(sError, err, False)
        else:
            msLogger.exception(sError, err, False)

        return JSONResponse(
            status_code=respStatusCode,
            content=jsonable_encoder(
                {
                    "detail": errorDetail
                }
            )
        )
    
@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    if settings.project.dev_mode:
        msLogger.exception(str(exc), exc, False)
        
    unprocessableEntity = HTTPStatus.UNPROCESSABLE_ENTITY
    supportRequestBody = False
    method = request.method
    if (settings.project.dev_mode) and ((method == "POST") or (method == "PUT") or (method == "DELETE")):
        reqContentType = request.headers.get("content-type")
        # only dump request body in dev mode !!!
        if (reqContentType is not None):
            if reqContentType.lower().find("application/json") >= 0:
                supportRequestBody = True

    # report only the first invalid
    error: dict[str, Any] | Any | None = exc.errors()[0]

    detail: dict[str, Any] = {
        "status_code": unprocessableEntity.value,
        "error": unprocessableEntity.phrase.upper(),
        "type": MsHTTPExceptionType.VALIDATION_ERROR,
        "message": unprocessableEntity.phrase,
        "timestamp": datetime.now(timezone.utc).replace(microsecond=0),
        "msg": unprocessableEntity.phrase
    }

    if (error is not None) and (isinstance(error, dict)):
        resp = FastApiParseError(error) # type: ignore
        if resp is not None:
            detail.update(
                type=resp.get("type"),
                message=resp.get("message"),
                loc=error.get("loc"), # use location from error # type: ignore
                field=resp.get("field"),
                msg=resp.get("msg")
            )
            ctx = resp.get("ctx")
            if ctx is not None:
                detail.update(ctx=ctx)
    
    if settings.project.dev_mode:
        detail.update(
            method=request.method,
            path=request.url.path,
            query_params=request.query_params,
            errors=jsonable_encoder(exc.errors(), exclude={"url"})
        )
        if supportRequestBody:
            detail.update(body=exc.body)
    return JSONResponse(
        status_code=unprocessableEntity.value,
        content=jsonable_encoder({"detail": detail})
    )

# Trusted Host Middleware
allow_origins = settings.config.allow_origins
if len(allow_origins) == 0:
    allow_origins.append("*")

hostHeaderName = "host"
if settings.config.behindNAT:
    if settings.config.proxyHostHeaderName is not None:
        hostHeaderName = settings.config.proxyHostHeaderName

app.add_middleware(
    MsTrustedHostMiddleware,
    allowed_hosts=settings.config.allowed_hosts,
    hostHeaderName=hostHeaderName,
    behindNAT=settings.config.behindNAT,
    proxyIpAddressHeaderName=settings.config.proxyIpAddressHeaderName,
    allowLoopbackIp=True,
    allowPrivateIp=True,
    debug=settings.project.dev_mode
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["DELETE", "GET", "HEAD", "OPTIONS", "POST", "PUT", "PATCH"],
    allow_headers=["*"],
)

if apmClient is not None:
    app.add_middleware(ElasticAPM, client=apmClient)

    @app.post(
        rootPath + "/send_to_apm",
        operation_id="send_to_apm",
        openapi_extra={
            "x-ignore": True
        }
    )
    async def send_to_apm(
        message: str = Body(
            default=...,
            embed=True,
            examples=["Hello"]
        )
    ):
        """
        Test send message
        """

        message = message.strip()
        message = datetime.now().isoformat() + " - " + message
        apmClient.capture_message(message) # type: ignore
        return {"status": message}
    
    @app.get(
        rootPath + "/test_pembagian",
        operation_id="test_pembagian",
        openapi_extra={
            "x-ignore": True
        }
    )
    async def error_test(x: int, y: int):
        """
        Test error. Contoh pembagian dengan 0
        """

        z = x / y
        return {"query": z}

@app.get(
    rootPath + "/health",
    operation_id="health",
    response_model=dict,
    response_description="Server status",
    openapi_extra={
        "x-ignore": True
    }
)
async def health():
    """
    Health check
    """

    return {"status": "ok"}

@app.get(
    path=rootPath + "/private/db_health",
    operation_id="db_health",
    response_model=dict,
    response_description="Database status"
)
async def db_health():
    """
    Ping database server
    """

    resp = {
        "response": None
    }
    try:
        resp = await MGDB.command("ping")
        if settings.project.dev_mode:
            msLogger.success("ping: " + json.dumps(jsonable_encoder(resp), indent=2))
        status = SuccessMessage.OK
    except Exception as err:
        if settings.project.dev_mode:
            status = SuccessMessage.FAILED
            if isinstance(err, OperationFailure):
                resp: dict[str, Any] = {
                    "details": err.details,
                    "timeout": err.timeout
                }
            elif isinstance(err, ServerSelectionTimeoutError):
                resp =  {
                    "details": err.details,
                    "message": str(err),
                    "timeout":  err.timeout
                }
                status = "TIMEOUT"
            else:
                resp = {
                    "details": str(err),
                    "type": str(type(err))
                }
        else:
            msLogger.exception(str(err), err, False)
            status = "Database error, check exception log"

    try:
        response = jsonable_encoder(resp)
    except:
        response = {
            "response": "Failed decode ping response"
        }
    ret: dict[str, Any] = {
        "status": status,
        "response": response
    }
    return ret

@app.get(
    rootPath + "/private/request_headers",
    operation_id="request_headers",
    response_model=dict,
    summary="Request headers"
)
async def GetRequestHeader(request: Request):
    headers = [{key: value} for key, value in request.headers.items()]

    ipAddress = OtherUtil.GetIpAddress(
        request,
        behindNAT=settings.config.behindNAT,
        proxyIpAddressHeaderName=settings.config.proxyIpAddressHeaderName
    )
    if not ipAddress:
        ipAddress = ""
        
    headers.append(
        {
            "ms_ipaddress": ipAddress
        }
    )
    return {
        "headers": headers
    }

if settings.config.installation:
    from routers.routerInstallation import ApiRouter_Install
    app.include_router(ApiRouter_Install, prefix=rootPath)

#--------------------------------------------------------------------- begin routers
# imports
# sales
from routers.master_data.routerMasterData import ApiRouter_Master_Data
from routers.master_data.routerMasterDataFollower import ApiRouter_Master_Data_Follower
from routers.uom.routerUoMCategory import ApiRouter_UoM_Category
from routers.uom.routerUoM import ApiRouter_UoM
from routers.generic_material.routerGenericMaterialCategory import ApiRouter_Generic_Material_Category
# Follower Endpoint


# routers implementation
# sales
app.include_router(ApiRouter_Master_Data, prefix=rootPath)
app.include_router(ApiRouter_Master_Data_Follower, prefix=rootPath)
app.include_router(ApiRouter_UoM_Category, prefix=rootPath)
app.include_router(ApiRouter_UoM, prefix=rootPath)
app.include_router(ApiRouter_Generic_Material_Category, prefix=rootPath)

# Follower Endpoint


#--------------------------------------------------------------------- end routers

from rabbitmq.handlers.user_service.consumer_user_service import *