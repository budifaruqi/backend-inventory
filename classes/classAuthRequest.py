import binascii
from enum import Enum
from typing import Any, Dict, Optional, Union, cast
from fastapi import Request
from fastapi.openapi.models import (
    HTTPBearer as HTTPBearerModel,
    APIKey, APIKeyIn,
    HTTPBase as HTTPBaseModel,
    OAuth2 as OAuth2Model,
    OAuthFlows as OAuthFlowsModel
)
from fastapi.security.base import SecurityBase
from fastapi.security.http import HTTPBase
from fastapi.security.api_key import APIKeyBase
from fastapi.security.utils import get_authorization_scheme_param
from utils.util_http_exception import MsHTTPForbiddenException, MsHTTPUnauthorizedException
from utils.util_http_response import MsHTTPExceptionMessage, MsHTTPExceptionType
from utils.security.ms_security import MsSecurity

class MsHeaderError(str, Enum):
    EMPTY_PARAM = "EMPTY_PARAM"
    INVALID_PARAM = "INVALID_PARAM"

class MsHTTPBearerCredential:
    def __init__(self, scheme: str, credentials: str, request: Request) -> None:
        self.scheme = scheme
        self.credentials = credentials
        self.request = request

class MsHTTPBearer(HTTPBase):
    def __init__(
        self,
        *,
        bearerFormat: Optional[str] = None,
        scheme_name: Optional[str] = None,
        description: Optional[str] = None
    ):
        self.model = HTTPBearerModel(bearerFormat=bearerFormat, description=description)
        self.scheme_name = scheme_name or self.__class__.__name__

    async def __call__( # type: ignore
        self, request: Request
    ):
        authorization = request.headers.get("Authorization")
        scheme, credentials = get_authorization_scheme_param(authorization)
        if not (authorization and scheme and credentials):
            raise MsHTTPForbiddenException(
                type=MsHTTPExceptionType.NOT_AUTHENTICATED,
                message=MsHTTPExceptionMessage.NOT_AUTHENTICATED
            )
        if scheme.lower() != "bearer":
            raise MsHTTPForbiddenException(
                type=MsHTTPExceptionType.INVALID_AUTHENTICATION_CREDENTIALS,
                message=MsHTTPExceptionMessage.INVALID_AUTHENTICATION_CREDENTIALS
            )
        credentials = credentials.strip()
        if len(credentials) == 0:
            raise MsHTTPForbiddenException(
                type=MsHTTPExceptionType.INVALID_AUTHENTICATION_CREDENTIALS,
                message=MsHTTPExceptionMessage.INVALID_AUTHENTICATION_CREDENTIALS
            )
        return MsHTTPBearerCredential(
            scheme=scheme,
            credentials=credentials,
            request=request
        )
        
# ========================================================

class MsHTTPApiKeyHeader:
    def __init__(self, credentials: str | None, request: Request) -> None:
        self.credentials = credentials
        self.request = request

class MsRequestAPIKeyHeader(APIKeyBase):
    def __init__(
        self,
        *,
        name: str,
        scheme_name: Optional[str] = None,
        description: Optional[str] = None
    ):
        self.model: APIKey = APIKey( # type: ignore
            **{"in": APIKeyIn.header},  # type: ignore[arg-type]
            name=name,
            description=description,
        )
        self.scheme_name = scheme_name or self.__class__.__name__

    async def __call__(self, request: Request) -> MsHeaderError | MsHTTPApiKeyHeader:
        api_key = request.headers.get(self.model.name)
        if not api_key:
            return MsHTTPApiKeyHeader(credentials=None, request=request)
        api_key = api_key.strip()
        if len(api_key) == 0:
            return MsHTTPApiKeyHeader(credentials=None, request=request)
        return MsHTTPApiKeyHeader(credentials=api_key, request=request)
    
# ========================================================

class MsHTTPBasicCredential:
    def __init__(
        self,
        username: str,
        password: str,
        realm: str | None,
        unauthorized_headers: dict[str, str],
        request: Request
    ) -> None:
        self.username: str = username
        self.password: str = password
        self.realm: str | None = realm
        self.unauthorized_headers = unauthorized_headers
        self.request: Request = request

class MsHTTPBasic(HTTPBase):
    def __init__(
        self,
        *,
        scheme_name: Optional[str] = None,
        realm: Optional[str] = None,
        description: Optional[str] = None
    ):
        self.model = HTTPBaseModel(scheme="basic", description=description)
        self.scheme_name = scheme_name or self.__class__.__name__
        self.realm = realm

    async def __call__(  # type: ignore
        self, request: Request
    ) -> MsHTTPBasicCredential:
        authorization = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if self.realm:
            unauthorized_headers = {"WWW-Authenticate": f'Basic realm="{self.realm}"'}
        else:
            unauthorized_headers = {"WWW-Authenticate": "Basic"}
        if (not authorization) or (not scheme) or (not param):
            raise MsHTTPUnauthorizedException(
                type=MsHTTPExceptionType.UNAUTHORIZED,
                message=MsHTTPExceptionMessage.NOT_AUTHENTICATED,
                headers=unauthorized_headers
            )
        if scheme.lower() != "basic":
            raise MsHTTPUnauthorizedException(
                type=MsHTTPExceptionType.UNAUTHORIZED,
                message=MsHTTPExceptionMessage.NOT_AUTHENTICATED,
                headers=unauthorized_headers
            )
        try:
            data = MsSecurity.b64decode_standard(param).decode("ascii")
        except (ValueError, UnicodeDecodeError, binascii.Error):
            raise MsHTTPUnauthorizedException(
                type=MsHTTPExceptionType.UNAUTHORIZED,
                message=MsHTTPExceptionMessage.INVALID_AUTHENTICATION_CREDENTIALS,
                headers=unauthorized_headers
            )
        username, separator, password = data.partition(":")
        if not separator:
            raise MsHTTPUnauthorizedException(
                type=MsHTTPExceptionType.UNAUTHORIZED,
                message=MsHTTPExceptionMessage.INVALID_AUTHENTICATION_CREDENTIALS,
                headers=unauthorized_headers
            )
        return MsHTTPBasicCredential(
            username=username,
            password=password,
            realm=self.realm,
            unauthorized_headers=unauthorized_headers,
            request=request
        )
    
# ========================================================

class MsOAuth2(SecurityBase):
    def __init__(
        self,
        *,
        flows: Union[OAuthFlowsModel, Dict[str, Dict[str, Any]]] = OAuthFlowsModel(),
        scheme_name: Optional[str] = None,
        description: Optional[str] = None
    ):
        self.model = OAuth2Model(
            flows=cast(OAuthFlowsModel, flows), description=description
        )
        self.scheme_name = scheme_name or self.__class__.__name__

    async def __call__(self, request: Request) -> Optional[str]:
        authorization = request.headers.get("Authorization")
        if not authorization:
            raise MsHTTPForbiddenException(
                type=MsHTTPExceptionType.NOT_AUTHENTICATED,
                message=MsHTTPExceptionMessage.NOT_AUTHENTICATED,
                headers={"WWW-Authenticate": "Bearer"}
            )
        return authorization

# ========================================================

class MsOAuth2PasswordBearerCredential:
    def __init__(self, scheme: str, credentials: str, request: Request) -> None:
        self.scheme: str = scheme
        self.credentials: str = credentials
        self.request: Request = request

class MsOAuth2PasswordBearer(MsOAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[Dict[str, str]] = None,
        description: Optional[str] = None
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(
            password=cast(Any, {"tokenUrl": tokenUrl, "scopes": scopes})
        )
        super().__init__(
            flows=flows,
            scheme_name=scheme_name,
            description=description
        )

    async def __call__(self, request: Request): # type: ignore
        authorization = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            raise MsHTTPUnauthorizedException(
                type=MsHTTPExceptionType.NOT_AUTHENTICATED,
                message=MsHTTPExceptionMessage.NOT_AUTHENTICATED,
                headers={"WWW-Authenticate": "Bearer"}
            )
        return MsOAuth2PasswordBearerCredential(
            scheme=scheme,
            credentials=param,
            request=request
        )

# ========================================================

