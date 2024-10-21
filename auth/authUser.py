import json
from typing import Annotated, Any
from fastapi import Depends
from fastapi.routing import APIRoute
from httpx import (
    RequestError as HttpxRequestError,
    ConnectTimeout as HttpxConnectTimeout
)
from classes.classAuthRequest import MsHTTPBearer, MsHTTPBearerCredential
from config.config import settings
from models.service_membership.enumRoleLocation import RoleLocation
from models.service_membership.modelMembershipAuth import ResponsVerifyEndpointServiceResult, VerifyEndpointServiceResult, VerifyEndpointCompanyResult, VerifyEndpointSystemResult
from models.shared.modelResponse import FailedResponseDetail
from utils.util_http_client import HttpClientDefault, IsJsonResponse
from utils.util_http_exception import MsHTTPException, MsHTTPExternalServerErrorException, MsHTTPForbiddenException, MsHTTPInternalServerErrorException, MsHTTPServiceUnavailableException
from utils.util_http_response import MsHTTPExceptionMessage, MsHTTPExceptionType
from utils.util_logger import msLogger


class AuthUser:

    BearerAuthenticationMethod = MsHTTPBearer(
        scheme_name="Account Bearer Authorization",
        description="Access token account"
    )

    BearerAuthenticationMethodAccountSystem = MsHTTPBearer(
        scheme_name="Account System Authorization",
        description="Akses token akun sistem"
    )
    
    BearerAuthenticationMethodAccountCompany = MsHTTPBearer(
        scheme_name="Account Company Authorization",
        description="Akses token akun perusahaan"
    )

    BearerAuthenticationMethodAccountExternal = MsHTTPBearer(
        scheme_name="Account External Authorization",
        description="Akses token akun external"
    )

    @staticmethod
    async def VerifyEndpoint(
        accessToken: str,
        serviceName: str,
        operationId: str
    ) -> VerifyEndpointServiceResult:
        url = settings.services.authService + "/private/account/verify_endpoint"
        try:
            reqBody: dict[str, Any] = {
                "serviceName": serviceName,
                "operationId": operationId
            }
            headers: dict[str, str] = {
                "Authorization": "Bearer " + accessToken
            }
            response = await HttpClientDefault().post(
                url=url,
                headers=headers,
                json=reqBody
            )
            isJsonResponse = IsJsonResponse(response)
            if response.status_code != 200:
                if isJsonResponse:
                    responseJsonFailed = response.json()
                    try:
                        verifyFail = FailedResponseDetail(**responseJsonFailed)
                    except:
                        if settings.project.dev_mode:
                            msLogger.error("VERIFY_MEMBERSHIP_AUTH_PRIVILEGE " + json.dumps(responseJsonFailed, indent=2))
                        raise MsHTTPException(
                            httpStatus=response.status_code,
                            error=None,
                            type=MsHTTPExceptionType.EXTERNAL_SERVER_ERROR_AUTH_SERVICE_INVALID_FAILED_RESPONSE,
                            message="Eksternal server authentikasi bermasalah",
                            debug={
                                "response": responseJsonFailed
                            }
                        )
                    
                    raise MsHTTPException(
                        httpStatus=response.status_code,
                        error=verifyFail.detail.error,
                        type=verifyFail.detail.type,
                        message=verifyFail.detail.message,
                        additionalData=verifyFail.detail.additionalData,
                        debug=verifyFail.detail.debug,
                        timestamp=verifyFail.detail.timestamp
                    )
                else:
                    try:
                        rawResponse = response.text
                    except:
                        rawResponse = "Gagal membaca raw response"
                    if settings.project.dev_mode:
                        msLogger.error("VERIFY_MEMBERSHIP_AUTH_PRIVILEGE " + rawResponse)
                    raise MsHTTPExternalServerErrorException(
                        type=MsHTTPExceptionType.EXTERNAL_SERVER_ERROR_AUTH_SERVICE,
                        message="Eksternal server authentikasi bermasalah",
                        debug={
                            "response": rawResponse
                        }
                    )
            else:
                if not isJsonResponse:
                    try:
                        rawResponse = response.text
                    except:
                        rawResponse = "Gagal membaca raw response"
                    raise MsHTTPExternalServerErrorException(
                        type=MsHTTPExceptionType.EXTERNAL_SERVER_ERROR_AUTH_SERVICE,
                        message="Eksternal server authentikasi bermasalah",
                        debug={
                            "response": rawResponse
                        }
                    )
                else:
                    responseJsonSuccess = response.json()
                    try:
                        verifySuccess = ResponsVerifyEndpointServiceResult(**responseJsonSuccess)
                        return verifySuccess.data
                    except:
                        raise MsHTTPExternalServerErrorException(
                            type=MsHTTPExceptionType.EXTERNAL_SERVER_ERROR_AUTH_SERVICE_INVALID_SUCCESS_RESPONSE,
                            message="Gagal menguraikan respon verifikasi dari server authentikasi",
                            debug={
                                "response": responseJsonSuccess
                            }
                        )
        except HttpxConnectTimeout:
            if settings.project.dev_mode:
                msLogger.error(MsHTTPExceptionType.EXTERNAL_SERVER_ERROR_AUTH_SERVICE.value + ". Connection timeout")
            raise MsHTTPServiceUnavailableException(
                type=MsHTTPExceptionType.AUTH_SERVICE_UNAVAILABLE,
                message="Koneksi ke server authentikasi timeout"
            )
                    
        except HttpxRequestError as exc:
            if settings.project.dev_mode:
                msLogger.error(MsHTTPExceptionType.EXTERNAL_SERVER_ERROR_AUTH_SERVICE.value + ". Request error " + str(exc.request.url))
            raise MsHTTPServiceUnavailableException(
                type=MsHTTPExceptionType.AUTH_SERVICE_UNAVAILABLE,
                message="Permintaan verifikasi ke server authentikasi terjadi masalah"
            )
        
        except Exception as err:
            if isinstance(err, MsHTTPException):
                raise err
            else:
                if settings.project.dev_mode:
                    s = str(err)
                    msLogger.error(MsHTTPExceptionType.INTERNAL_SERVER_ERROR.value + ". Error " + s)
                else:
                    s = MsHTTPExceptionMessage.INTERNAL_SERVER_ERROR.value

                raise MsHTTPInternalServerErrorException(
                    type="VERIFY_CREDENTIAL",
                    message=s
                )

class AuthUserDep:
    """
    User Authentication Dependency
    """
    
    @staticmethod
    async def VerifyEndpoint(
        authorization: Annotated[MsHTTPBearerCredential, Depends(AuthUser.BearerAuthenticationMethod)]
    ) -> VerifyEndpointServiceResult:
        route: APIRoute | Any | None = authorization.request.scope.get("route")
        if (route is None) or (not isinstance(route, APIRoute)):
            raise MsHTTPInternalServerErrorException(
                "INVALID_ROUTE_CLASS",
                f"Endpoint bukan turunan dari class {APIRoute.__name__}",
                debug={
                    "type": str(route)
                }
            )
        operationId = route.operation_id
        if operationId is None:
            raise MsHTTPInternalServerErrorException(
                "EMPTY_OPERATION_ID",
                f"Endpoint tidak mempunyai id operasi (operationId)",
                debug={
                    "type": str(route)
                }
            )
        serviceName = settings.project.serviceName
        if route.openapi_extra is not None:
            mService: str | Any | None = route.openapi_extra.get("x-service")
            if (mService is not None) and (isinstance(mService, str)):
                serviceName = mService
        return await AuthUser.VerifyEndpoint(
            authorization.credentials,
            serviceName,
            operationId
        )
    
    @staticmethod
    async def VerifyEndpointCompany(
        authorization: Annotated[MsHTTPBearerCredential, Depends(AuthUser.BearerAuthenticationMethodAccountCompany)]
    ) -> VerifyEndpointCompanyResult:
        route: APIRoute | Any | None = authorization.request.scope.get("route")
        if (route is None) or (not isinstance(route, APIRoute)):
            raise MsHTTPInternalServerErrorException(
                "INVALID_ROUTE_CLASS",
                f"Endpoint bukan turunan dari class {APIRoute.__name__}",
                debug={
                    "type": str(route)
                }
            )
        operationId = route.operation_id or route.unique_id
        serviceName = settings.project.serviceName
        if route.openapi_extra is not None:
            mService: str | Any | None = route.openapi_extra.get("x-service")
            if (mService is not None) and (isinstance(mService, str)):
                serviceName = mService

        verifyResult = await AuthUser.VerifyEndpoint(
            authorization.credentials,
            serviceName,
            operationId
        )
        if (verifyResult.roleLocation != RoleLocation.company) or (verifyResult.companyId is None) or (verifyResult.companyCategoryId is None):
            raise MsHTTPForbiddenException(
                MsHTTPExceptionType.CREDENTIAL_LOCATION_SYSTEM_FORBIDDEN,
                MsHTTPExceptionMessage.CREDENTIAL_LOCATION_SYSTEM_FORBIDDEN,
                additionalData={
                    "serviceName": serviceName,
                    "operationId": operationId
                }
            )
        return VerifyEndpointCompanyResult(
            accountId=verifyResult.accountId,
            roleClaimed=verifyResult.roleClaimed,
            roleName=verifyResult.roleName,
            companyCategoryId=verifyResult.companyCategoryId,
            companyId=verifyResult.companyId
        )
    
    @staticmethod
    async def VerifyEndpointSystem(
        authorization: Annotated[MsHTTPBearerCredential, Depends(AuthUser.BearerAuthenticationMethodAccountSystem)]
    ) -> VerifyEndpointSystemResult:
        route: APIRoute | Any | None = authorization.request.scope.get("route")
        if (route is None) or (not isinstance(route, APIRoute)):
            raise MsHTTPInternalServerErrorException(
                "INVALID_ROUTE_CLASS",
                f"Endpoint bukan turunan dari class {APIRoute.__name__}",
                debug={
                    "type": str(route)
                }
            )
        operationId = route.operation_id
        if operationId is None:
            raise MsHTTPInternalServerErrorException(
                "EMPTY_OPERATION_ID",
                f"Endpoint tidak mempunyai id operasi (operationId)",
                debug={
                    "type": str(route)
                }
            )
        serviceName = settings.project.serviceName
        if route.openapi_extra is not None:
            mService: str | Any | None = route.openapi_extra.get("x-service")
            if (mService is not None) and (isinstance(mService, str)):
                serviceName = mService

        verifyResult = await AuthUser.VerifyEndpoint(
            authorization.credentials,
            serviceName,
            operationId
        )
        if (verifyResult.roleLocation != RoleLocation.system) or (verifyResult.companyId is not None) or (verifyResult.companyCategoryId is not None):
            raise MsHTTPForbiddenException(
                MsHTTPExceptionType.CREDENTIAL_LOCATION_COMPANY_FORBIDDEN,
                MsHTTPExceptionMessage.CREDENTIAL_LOCATION_COMPANY_FORBIDDEN,
                additionalData={
                    "serviceName": serviceName,
                    "operationId": operationId
                }
            )
        return VerifyEndpointSystemResult(
            accountId=verifyResult.accountId,
            roleClaimed=verifyResult.roleClaimed,
            roleName=verifyResult.roleName
        )
