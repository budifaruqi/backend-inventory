from datetime import datetime, timezone
from http import HTTPStatus
from typing import Any, Dict, Optional

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from config.config import settings
from models.shared.modelDataType import BaseModel
from utils.util_http_response import MsHTTPExceptionType


class MsHTTPException(HTTPException):
    def __init__(
        self,
        httpStatus: HTTPStatus | int,
        *,
        error: Optional[str] = None,
        type: Optional[str] = None,
        message: Optional[str] = None,
        headers: Optional[Dict[str, Any]] = None,
        additionalData: Optional[Dict[str, Any] | BaseModel] = None,
        debug: Optional[Dict[str, Any] | BaseModel] = None,
        timestamp: Optional[datetime] = None
    ) -> None:
        """
        Base MsHTTPException
        """
        if isinstance(httpStatus, HTTPStatus):
            statusCode = httpStatus.value
            if error is None:
                phrase = httpStatus.phrase.upper()
            else:
                phrase = error
            if message is None:
                message = httpStatus.description
            elif len(message) == 0:
                message = httpStatus.description
        else:
            statusCode = httpStatus
            if error is not None:
                phrase = error
                if (message is None) or (len(message) == 0):
                    try:
                        hStatus = HTTPStatus(statusCode)
                        message = hStatus.description
                    except:
                        message = ""
            else:
                try:
                    hStatus = HTTPStatus(statusCode)
                    phrase = hStatus.phrase.upper()
                    if (message is None) or (len(message) == 0):
                        message = hStatus.description
                except:
                    phrase = ""
            if message is None:
                message = ""
        if type is None:
            type = phrase

        self.httpStatus = statusCode
        self.error = phrase
        self.type = type
        self.message = message
        self.headers = headers or {}
        self.timestamp = timestamp
        if self.timestamp is None:
            self.timestamp = datetime.now(timezone.utc).replace(microsecond=0)

        detail: dict[str, Any] = {
            "status_code": statusCode,
            "error": phrase,
            "type": type,
            "message": message,
            "timestamp": self.timestamp
        }
        if additionalData is not None:
            if isinstance(additionalData, BaseModel):
                additionalData =  additionalData.model_dump()

            detail["additionalData"] = jsonable_encoder(additionalData)

        if (debug is not None):
            if isinstance(debug, BaseModel):
                debug = debug.model_dump(mode="json")
            debug = jsonable_encoder(debug)
            if settings.project.dev_mode:
                detail["debug"] = debug

        self.additionalData = additionalData
        self.debug = debug

        super().__init__(
            status_code=statusCode,
            detail=jsonable_encoder(detail),
            headers=headers
        )

    def GetErrorMessage(self) -> str | None:
        sError = None
        if isinstance(self.detail, dict):
            rawError = self.detail.get("message") # type: ignore
            if (rawError is not None) and (isinstance(rawError, str)):
                sError = rawError
        if (sError is None) and (self.detail is not None) and (isinstance(self.detail, str)): # type: ignore
            sError = str(self.detail)
        return sError
    
    def GetErrorType(self) -> str:
        if self.detail is not None: # type: ignore
            if isinstance(self.detail, dict):
                t = self.detail.get("type") # type: ignore
                if (t is not None) and (isinstance(t, str)):
                    return t
        return "ERROR"

    def __str__(self) -> str:
        e = self.GetErrorMessage()
        hasE = (e is not None) and (e != "")
        t = self.GetErrorType()
        ret = ""
        ret += t
        if hasE:
            ret += " - "
        if hasE and (e is not None):
            ret += e
        return ret
    
    def Json(self) -> dict[str, Any]:
        detail: dict[str, Any] = {
            "status_code": self.httpStatus,
            "error": self.error,
            "type": self.type,
            "message": self.message,
            "timestamp": self.timestamp
        }
        if self.additionalData is not None:
            detail["additionalData"] = self.additionalData
        if (settings.project.dev_mode) and (self.debug is not None):
            detail["debug"] = self.debug

        return jsonable_encoder(detail)

class MsHTTPBadRequestException(MsHTTPException):
    def __init__(
        self,
        type: str = MsHTTPExceptionType.BAD_REQUEST.value,
        message: Optional[str] = None,
        headers: Optional[Dict[str, Any]] = None,
        additionalData: Optional[Dict[str, Any] | BaseModel] = None,
        debug: Optional[Dict[str, Any] | BaseModel] = None
    ) -> None:
        """
        Error 400
        """
        super().__init__(
            HTTPStatus.BAD_REQUEST,
            type=type,
            message=message,
            headers=headers,
            additionalData=additionalData,
            debug=debug
        )

class MsHTTPUnauthorizedException(MsHTTPException):
    def __init__(
        self,
        type: str = MsHTTPExceptionType.UNAUTHORIZED.value,
        message: Optional[str] = None,
        headers: Optional[Dict[str, Any]] = None,
        additionalData: Optional[Dict[str, Any] | BaseModel] = None,
        debug: Optional[Dict[str, Any] | BaseModel] = None
    ) -> None:
        """
        Error 401
        """
        super().__init__(
            HTTPStatus.UNAUTHORIZED,
            type=type,
            message=message,
            headers=headers,
            additionalData=additionalData,
            debug=debug
        )

class MsHTTPForbiddenException(MsHTTPException):
    def __init__(
        self,
        type: str = MsHTTPExceptionType.FORBIDDEN.value,
        message: Optional[str] = None,
        headers: Optional[Dict[str, Any]] = None,
        additionalData: Optional[Dict[str, Any] | BaseModel] = None,
        debug: Optional[Dict[str, Any] | BaseModel] = None
    ) -> None:
        """
        Error 403
        """
        super().__init__(
            HTTPStatus.FORBIDDEN,
            type=type,
            message=message,
            headers=headers,
            additionalData=additionalData,
            debug=debug
        )

class MsHTTPNotFoundException(MsHTTPException):
    def __init__(
        self,
        type: str = MsHTTPExceptionType.NOT_FOUND.value,
        message: Optional[str] = None,
        headers: Optional[Dict[str, Any]] = None,
        additionalData: Optional[Dict[str, Any] | BaseModel] = None,
        debug: Optional[Dict[str, Any] | BaseModel] = None
    ) -> None:
        """
        Error 404
        """
        super().__init__(
            HTTPStatus.NOT_FOUND,
            type=type,
            message=message,
            headers=headers,
            additionalData=additionalData,
            debug=debug
        )

class MsHTTPConflictException(MsHTTPException):
    def __init__(
        self,
        type: str = MsHTTPExceptionType.CONFLICT.value,
        message: Optional[str] = None,
        headers: Optional[Dict[str, Any]] = None,
        additionalData: Optional[Dict[str, Any] | BaseModel] = None,
        debug: Optional[Dict[str, Any] | BaseModel] = None
    ) -> None:
        """
        Error 409
        """
        super().__init__(
            HTTPStatus.CONFLICT,
            type=type,
            message=message,
            headers=headers,
            additionalData=additionalData,
            debug=debug
        )

class MsHttpRequestEntityTooLargeException(MsHTTPException):
    def __init__(
        self,
        type: str = MsHTTPExceptionType.REQUEST_ENTITY_TOO_LARGE.value,
        message: Optional[str] = None,
        headers: Optional[Dict[str, Any]] = None,
        additionalData: Optional[Dict[str, Any] | BaseModel] = None,
        debug: Optional[Dict[str, Any] | BaseModel] = None
    ) -> None:
        """
        Error 413
        """
        super().__init__(
            HTTPStatus.REQUEST_ENTITY_TOO_LARGE,
            type=type,
            message=message,
            headers=headers,
            additionalData=additionalData,
            debug=debug
        )

class MsHttpUnsupportedMediaTypeException(MsHTTPException):
    def __init__(
        self,
        type: str = MsHTTPExceptionType.UNSUPPORTED_MEDIA_TYPE.value,
        message: Optional[str] = None,
        headers: Optional[Dict[str, Any]] = None,
        additionalData: Optional[Dict[str, Any] | BaseModel] = None,
        debug: Optional[Dict[str, Any] | BaseModel] = None
    ) -> None:
        """
        Error 415
        """
        super().__init__(
            HTTPStatus.UNSUPPORTED_MEDIA_TYPE,
            type=type,
            message=message,
            headers=headers,
            additionalData=additionalData,
            debug=debug
        )

class MsHTTPTooManyRequestException(MsHTTPException):
    def __init__(
        self,
        type: str = MsHTTPExceptionType.TOO_MANY_REQUESTS.value,
        message: Optional[str] = None,
        headers: Optional[Dict[str, Any]] = None,
        additionalData: Optional[Dict[str, Any] | BaseModel] = None,
        debug: Optional[Dict[str, Any] | BaseModel] = None
    ) -> None:
        """
        Error 429
        """
        super().__init__(
            HTTPStatus.TOO_MANY_REQUESTS,
            type=type,
            message=message,
            headers=headers,
            additionalData=additionalData,
            debug=debug
        )

class MsHTTPInternalServerErrorException(MsHTTPException):
    def __init__(
        self,
        type: str = MsHTTPExceptionType.INTERNAL_SERVER_ERROR.value,
        message: Optional[str] = None,
        headers: Optional[Dict[str, Any]] = None,
        additionalData: Optional[Dict[str, Any] | BaseModel] = None,
        debug: Optional[Dict[str, Any] | BaseModel] = None
    ) -> None:
        """
        Error 500
        """
        super().__init__(
            HTTPStatus.INTERNAL_SERVER_ERROR,
            type=type,
            message=message,
            headers=headers,
            additionalData=additionalData,
            debug=debug
        )

class MsHTTPExternalServerErrorException(MsHTTPException):
    def __init__(
        self,
        type: str = MsHTTPExceptionType.EXTERNAL_SERVER_ERROR.value,
        message: Optional[str] = None,
        headers: Optional[Dict[str, Any]] = None,
        additionalData: Optional[Dict[str, Any] | BaseModel] = None,
        debug: Optional[Dict[str, Any] | BaseModel] = None
    ) -> None:
        """
        Error 500
        """
        super().__init__(
            HTTPStatus.INTERNAL_SERVER_ERROR,
            type=type,
            message=message,
            headers=headers,
            additionalData=additionalData,
            debug=debug
        )

class MsHTTPNotImplementedException(MsHTTPException):
    def __init__(
        self,
        type: str = MsHTTPExceptionType.NOT_IMPLEMENTED.value,
        message: Optional[str] = None,
        headers: Optional[Dict[str, Any]] = None,
        additionalData: Optional[Dict[str, Any] | BaseModel] = None,
        debug: Optional[Dict[str, Any] | BaseModel] = None
    ) -> None:
        """
        Error 501
        """
        super().__init__(
            HTTPStatus.NOT_IMPLEMENTED,
            type=type,
            message=message,
            headers=headers,
            additionalData=additionalData,
            debug=debug
        )

class MsHTTPServiceUnavailableException(MsHTTPException):
    def __init__(
        self,
        type: str = MsHTTPExceptionType.SERVICE_UNAVAILABLE.value,
        message: Optional[str] = None,
        headers: Optional[Dict[str, Any]] = None,
        additionalData: Optional[Dict[str, Any] | BaseModel] = None,
        debug: Optional[Dict[str, Any] | BaseModel] = None
    ) -> None:
        """
        Error 503
        """
        super().__init__(
            HTTPStatus.SERVICE_UNAVAILABLE,
            type=type,
            message=message,
            headers=headers,
            additionalData=additionalData,
            debug=debug
        )