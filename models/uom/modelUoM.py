from pydantic import Field
from models.shared.modelDataType import BaseModel, ObjectId
from models.shared.modelPagination import MsPaginationResult
from models.shared.modelResponse import ResponseModel
from models.shared.modelAuditData import AuditData

def UoMType 

class UoMBase(BaseModel):
    name: str = Field(
        default=...,
        title="Name",
        examples=["Pcs"]
    )
    type: UoMType = 

class UoMCategoryEx(UoMCategoryBase):
    companyId: ObjectId = Field(
        ...,
        title="Company Id"
    )
# --------------------------------------------------------------------------
class LeadInDb(AuditData,UoMCategoryEx):
    id: ObjectId = Field(
        default=...,
        alias="_id",
        title="Unit Of Measure Id"
    )

class UoMCategoryCreateWebRequest(UoMCategoryBase):
    pass

class UoMCategoryCreateCommandRequest(AuditData, UoMCategoryEx):
    pass

# --------------------------------------------------------------------------
class UoMCategoryView(UoMCategoryEx):
    id: ObjectId = Field(
        default=...,
        alias="_id",
        title="Unit Of Measure Id"
    )

class ResponseUoMCategoryView(ResponseModel):
    data: UoMCategoryView

class ResponsePagingUoMCategoryView(ResponseModel):
    data: MsPaginationResult[UoMCategoryView]

class ResponseComboUoMCategoryView(ResponseModel):
    data: list[UoMCategoryView]

# --------------------------------------------------------------------------
