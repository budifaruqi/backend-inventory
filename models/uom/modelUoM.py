from pydantic import Field
from models.shared.modelDataType import BaseModel, ObjectId
from models.shared.modelPagination import MsPaginationResult
from models.shared.modelResponse import ResponseModel
from models.shared.modelAuditData import AuditData
from models.uom.enumUoM import UoMType

class UoMBase(BaseModel):
    name: str = Field(
        default=...,
        title="Name",
        examples=["Pcs"]
    )
    type: UoMType = Field(
        ...,
        title="Type",
        examples=["REFERENCE","SMALLER", "BIGGER"]
    )
    ratio: float = Field(
        ...,
        title="Ratio"
    )
    isActive: bool = Field(
        True,
        title="Active"
    )

class UoMEx(UoMBase):
    companyId: ObjectId = Field(
        ...,
        title="Company Id"
    )
# --------------------------------------------------------------------------
class UoMInDb(AuditData,UoMEx):
    id: ObjectId = Field(
        default=...,
        alias="_id",
        title="Unit Of Measure Id"
    )

class UoMCreateWebRequest(UoMBase):
    categoryId: ObjectId = Field(
        ...,
        title="UoM Category Id"
    )

class UoMCreateCommandRequest(AuditData, UoMEx):
    categoryId: ObjectId = Field(
        ...,
        title="UoM Category Id"
    )

# --------------------------------------------------------------------------
class UoMView(UoMEx):
    id: ObjectId = Field(
        default=...,
        alias="_id",
        title="Unit Of Measure Id"
    )

class ResponseUoMView(ResponseModel):
    data: UoMView

class ResponsePagingUoMView(ResponseModel):
    data: MsPaginationResult[UoMView]

class ResponseComboUoMView(ResponseModel):
    data: list[UoMView]

# --------------------------------------------------------------------------
