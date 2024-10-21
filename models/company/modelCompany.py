from typing import List
from pydantic import Field

from models.shared.modelDataType import BaseModel, ObjectId
from models.shared.modelPagination import MsPaginationResult
from models.shared.modelResponse import ResponseModel
from models.company.modelCompanyConfig import CompanyConfig
from models.shared.modelAuditData import AuditData
from models.shared.modelSample import SampleModel


class CompanyDetail(BaseModel):
    """
    Detail perusahaan
    """
    
    name: str = Field(
        default=...,
        title="Nama",
        description="Nama perusahaan",
        examples=["PT Contoh"]
    )
    initial: str = Field(
        default=...,
        title="Inisial",
        description="Nama inisial perusahaan [a..z][0..9][-_.]",
        examples=["pt_contoh"]
    )

class CompanyEx(BaseModel):
    """
    Extended Detail perusahaan
    """

    isActive: bool = Field(
        default=...,
        title="Aktif",
        description="Status keaktifan perusahaan",
        examples=[True]
    )
    companyCategoryId: ObjectId = Field(
        default=...,
        title="Id Kategori Perusahaan",
        description="Id kategori perusahaan",
        examples=[SampleModel.objectId_str_1]
    )

class CompanyCreateParam(AuditData, CompanyConfig, CompanyEx, CompanyDetail):
    """
    Main Model
    """
    pass

# --------------------------------------------------------------------------

class CompanyView(CompanyEx, CompanyDetail):
    id: ObjectId = Field(
        default=...,
        alias="_id",
        title="Id Perusahaan",
        description="Id perusahaan (companyId)"
    )
    """
    companyId
    """

class ResponseCompanyView(ResponseModel):
    data: CompanyView

class ResponsePagingCompanyView(ResponseModel):
    data: MsPaginationResult[CompanyView]

# --------------------------------------------------------------------------

class CompanyViewEx(CompanyView):
    companyCategoryName: str = Field(
        default="",
        title="Nama kategori perusahaan",
        examples=["TKI FTP"]
    )

class ResponseCompanyViewEx(ResponseModel):
    data: CompanyViewEx
    accountId: ObjectId = Field(
        default=...,
        description="Id akun",
        examples=[SampleModel.objectId_str_AA]
    )

class ResponsePagingCompanyViewEx(ResponseModel):
    data: MsPaginationResult[CompanyViewEx]

# --------------------------------------------------------------------------

class CompanyDetailId(CompanyDetail):
    id: ObjectId = Field(
        default=...,
        alias="_id",
        title="Id Perusahaan",
        description="Id perusahaan (companyId)"
    )
    """
    companyId
    """

class ResponseCompanyDetailId(ResponseModel):
    data: CompanyDetailId

class ResponseListCompanyDetailId(ResponseModel):
    data: List[CompanyDetailId]

# --------------------------------------------------------------------------

class CompanyName(BaseModel):
    """
    Detail perusahaan
    """
    
    name: str = Field(
        default=...,
        title="Nama",
        description="Nama perusahaan",
        examples=["PT Contoh"]
    )
    id: ObjectId = Field(
        default=...,
        alias="_id",
        title="Id Perusahaan",
        description="Id perusahaan (companyId)"
    )
    """
    companyId
    """

class ResponseListCompanyName(ResponseModel):
    data: List[CompanyName]
