from typing import List
from pydantic import Field
from models.shared.modelAuditData import AuditData
from models.shared.modelDataType import BaseModel, BaseModelObjectId, ObjectId
from models.shared.modelPagination import MsPaginationResult
from models.shared.modelResponse import ResponseModel


class CompanyCategory(BaseModel):
    name: str = Field(
        default=...,
        title="Nama",
        description="Nama kategori perusahaan"
    )

class CompanyCategoryEx(CompanyCategory):
    isActive: bool = Field(
        default=...,
        title="Aktif",
        description="Status keaktifan kategori perusahaan",
        examples=[True]
    )

class CompanyCategoryCreate(AuditData, CompanyCategoryEx):
    """
    Main Model
    """
    pass

# --------------------------------------------------------------------------

class CompanyCategoryId(BaseModelObjectId, CompanyCategoryEx):
    id: ObjectId = Field(
        default=...,
        alias="_id",
        title="Id Kategori Perusahaan",
        description="Id kategori perusahaan (companyCategoryId)"
    )
    """
    companyCategoryId
    """

class ResponseCompanyCategoryId(ResponseModel):
    data: CompanyCategoryId

class ResponseListCompanyCategoryId(ResponseModel):
    data: List[CompanyCategoryId]

class ResponsePagingCompanyCategoryId(ResponseModel):
    data: MsPaginationResult[CompanyCategoryId]

# --------------------------------------------------------------------------
