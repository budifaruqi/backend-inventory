from datetime import datetime
from enum import Enum
from typing import Any, List
from pydantic import ConfigDict, Field

from models.shared.modelDataType import BaseModel, ObjectId


# Enum Response Message for error status code 2xx
class SuccessMessage(str, Enum):
    OK = "OK"
    FAILED =  "FAILED"
    SUCCESS_READ = "SUCCESS_READ"
    SUCCESS_CREATED = "SUCCESS_CREATED"
    SUCCESS_UPDATED = "SUCCESS_UPDATED"
    SUCCESS_UNCHANGED = "SUCCESS_UNCHANGED"
    SUCCESS_DELETED = "SUCCESS_DELETED"
    SUCCESS_LOGIN  = "SUCCESS_LOGIN"
    SUCCESS_LOGOUT  = "SUCCESS_LOGOUT"
    SUCCESS_REFRESH_TOKEN = "SUCCESS_REFRESH_TOKEN"
    SUCCESS_VALIDATE_PRIVILEGE = "SUCCESS_VALIDATE_PRIVILEGE"

    # place other success type from external service here

class ResponseModel(BaseModel):
    status_code: int = Field(
        default=200,
        examples=[200]
    )
    type: str = Field(
        default=SuccessMessage.OK.value,
        examples=[SuccessMessage.OK.value]
    )
    message: str = Field(
        default=SuccessMessage.OK.value
    )
    data: Any
    
    model_config = ConfigDict(extra='allow')

class ResponseModelString(ResponseModel):
    data: str

class ResponseModelBoolean(ResponseModel):
    data: bool

class ResponseModelInteger(ResponseModel):
    data: int

class ResponseModelObjectId(ResponseModel):
    data: ObjectId

class ResponseModelListString(ResponseModel):
    data: List[str]

# ---------------------------------------------------------------

class FailedResponse(BaseModel):
    status_code: int
    error: str
    type: str
    message: str = ""
    timestamp: datetime
    additionalData: dict[str, Any] | None = None
    debug: dict[str, Any] | None = None

class FailedResponseDetail(BaseModel):
    detail: FailedResponse

# ---------------------------------------------------------------
