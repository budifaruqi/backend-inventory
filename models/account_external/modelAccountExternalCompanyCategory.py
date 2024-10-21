from typing import List
from pydantic import Field
from models.shared.modelDataType import BaseModel, ObjectId
from models.shared.modelResponse import ResponseModel
from models.shared.modelSample import SampleModel


class AccountExternalCompanyCategory(BaseModel):
    companyCategoryId: ObjectId = Field(
        default=...,
        title="Id Kategori Perusahaan",
        description="Id kategori perusahaan",
        examples=[SampleModel.objectId_str_AA]
    )
    companyCategoryName: str = Field(
        default=...,
        title="Nama Kategori Perusahaan",
        description="Nama kategori perusahaan",
        examples=["Abcde"]
    )
    features: List[str] = Field(
        default=...,
        title="Daftar Fitur",
        description="Daftar fitur",
        examples=[["partner", "reseller"]],
        json_schema_extra={
            "example": ["partner", "reseller"]
        }
    )

# --------------------------------------------------------------------------

class ResponseAccountExternalCompanyCategory(ResponseModel):
    data: AccountExternalCompanyCategory

class ResponsePagingAccountExternalCompanyCategory(ResponseModel):
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
    data: List[AccountExternalCompanyCategory] = Field(
        default=...,
        description="Daftar kategori perusahaan"
    )

# --------------------------------------------------------------------------

