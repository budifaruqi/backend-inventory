from typing import List

from pydantic import Field
from models.shared.modelDataType import BaseModel, ObjectId
from models.shared.modelPagination import MsPaginationResult
from models.shared.modelResponse import ResponseModel
from models.shared.modelSample import SampleModel


class AccountCompany(BaseModel):
    companyId: ObjectId = Field(
        default=...,
        title="Id Perusahaan",
        description="Id perusahaan",
        examples=[SampleModel.objectId_str_AA]
    )
    companyName: str = Field(
        default=...,
        title="Nama Perusahaan",
        description="Nama perusahaan",
        examples=["PT Abcde"]
    )
    roles: List[ObjectId] = Field(
        default=...,
        title="Daftar peran hak akses",
        description="Daftar peran hak akses di lokasi perusahaan"
    )

class ResponseAccountCompany(ResponseModel):
    data: AccountCompany

class ResponsePagingAccountView(ResponseModel):
    data: MsPaginationResult[AccountCompany]

# ----------------------------------------------------

class AccountCompanyName(BaseModel):
    companyId: ObjectId = Field(
        default=...,
        title="Id Perusahaan",
        description="Id perusahaan",
        examples=[SampleModel.objectId_str_AA]
    )
    companyName: str = Field(
        default=...,
        title="Nama Perusahaan",
        description="Nama perusahaan",
        examples=["PT Abcde"]
    )

class ResponseAccountCompanyName(ResponseModel):
    data: AccountCompanyName

class ResponsePagingAccountCompanyName(ResponseModel):
    size: int = Field(
        default=...,
        description="Jumlah item per halaman",
        examples=[100]
    )
    page: int = Field(
        default=...,
        description="Nomor halaman",
        examples=[1]
    )
    total: int = Field(
        default=...,
        description="Total item.\n**Total hanya dikalkulasi jika `page` bernilai `1`.\nJika `page` bernilai lebih dari `1`, maka nilai `Total` akan selalu `-1`**",
        examples=[10]
    )
    data: List[AccountCompanyName] = Field(
        default=...,
        description="Daftar perusahaan"
    )

# ----------------------------------------------------

class AccountCompanyId(BaseModel):
    companyId: ObjectId = Field(
        default=...,
        title="Id Perusahaan",
        description="Id perusahaan",
        examples=[SampleModel.objectId_str_AA]
    )
