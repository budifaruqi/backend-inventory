from pydantic import Field

from models.shared.modelAuditData import AuditData
from models.shared.modelDataType import BaseModel, ObjectId
from models.shared.modelPagination import MsPaginationResult
from models.shared.modelResponse import ResponseModel


class GenericMaterialCategoryBase(BaseModel):
    name: str = Field(
        default=...,
        title="Name",
        examples=["Unit"]
    )

class GenericMaterialCategoryEx(GenericMaterialCategoryBase):
    companyId: ObjectId = Field(
        ...,
        title="Company Id"
    )
# --------------------------------------------------------------------------
class GenericMaterialCategoryInDb(AuditData,GenericMaterialCategoryEx):
    id: ObjectId = Field(
        default=...,
        alias="_id",
        title="Generic Material Category Id"
    )

class GenericMaterialCategoryCreateWebRequest(GenericMaterialCategoryBase):
    pass

class GenericMaterialCategoryCreateCommandRequest(AuditData, GenericMaterialCategoryEx):
    pass

# --------------------------------------------------------------------------
class GenericMaterialCategoryView(GenericMaterialCategoryEx):
    id: ObjectId = Field(
        default=...,
        alias="_id",
        title="Generic Material Id"
    )

class ResponseGenericMaterialCategoryView(ResponseModel):
    data: GenericMaterialCategoryView

class ResponsePagingGenericMaterialCategoryView(ResponseModel):
    data: MsPaginationResult[GenericMaterialCategoryView]

class ResponseComboGenericMaterialCategoryView(ResponseModel):
    data: list[GenericMaterialCategoryView]

# --------------------------------------------------------------------------
