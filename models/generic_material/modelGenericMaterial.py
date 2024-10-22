from pydantic import Field

from models.shared.modelAuditData import AuditData
from models.shared.modelDataType import BaseModel, ObjectId
from models.shared.modelPagination import MsPaginationResult
from models.shared.modelResponse import ResponseModel


class GenericMaterialBase(BaseModel):
    name: str = Field(
        default=...,
        title="Name",
        examples=["Unit"]
    )
    categoryId: ObjectId = Field(
        ...,
        title="Generic Material Category Id"
    )
    salesPrice: float = Field(
        ...,
        title="Sales Price"
    )
    cost: float = Field(
        ...,
        title="Cost"
    )
    uomId: ObjectId = Field(
        ...,
        title="Unit Of Measure"
    )

class GenericMaterialEx(GenericMaterialBase):
    companyId: ObjectId = Field(
        ...,
        title="Company Id"
    )
# --------------------------------------------------------------------------
class GenericMaterialInDb(AuditData,GenericMaterialEx):
    id: ObjectId = Field(
        default=...,
        alias="_id",
        title="Generic Material Id"
    )

class GenericMaterialCreateWebRequest(GenericMaterialBase):
    pass

class GenericMaterialCreateCommandRequest(AuditData, GenericMaterialEx):
    pass

# --------------------------------------------------------------------------
class GenericMaterialView(GenericMaterialEx):
    id: ObjectId = Field(
        default=...,
        alias="_id",
        title="Generic Material Id"
    )

class ResponseGenericMaterialView(ResponseModel):
    data: GenericMaterialView

class ResponsePagingGenericMaterialView(ResponseModel):
    data: MsPaginationResult[GenericMaterialView]

class ResponseComboGenericMaterialView(ResponseModel):
    data: list[GenericMaterialView]

# --------------------------------------------------------------------------
