from enum import Enum
from typing import List
from pydantic import EmailStr, Field
from models.account_external.modelAccountExternalCompanyCategory import AccountExternalCompanyCategory
from models.shared.modelDataType import BaseModel, ObjectId
from models.shared.modelPagination import MsPaginationResult2
from models.shared.modelResponse import ResponseModel


class AccountExternalDetail(BaseModel):
    """
    Detail akun eksternal
    """

    name: str = Field(
        default=...,
        title="Nama",
        description="Nama",
        examples=[
            "Taufik"
        ]
    )

class AccountExternalIdentity(BaseModel):
    username: str = Field(
        default=...,
        title="Nama Akun",
        description="Nama akun",
        examples=[
            "taufik"
        ]
    )
    email: EmailStr | None = Field(
        default=None,
        title="Email",
        description="Alamat email",
        examples=[
            "example@localhost.demo"
        ]
    )
    phone: str | None = Field(
        default=None,
        title="Phone",
        description="Nomor telepon",
        examples=[
            "081226526666"
        ]
    )

class AccountExternalPrivilege(BaseModel):
    """
    Hak akses akun
    """
    companyCategoryIds: List[AccountExternalCompanyCategory] = Field(
        default=...,
        title="Daftar kategori Perusahaan",
        description="Daftar kategori perusahaan"
    )

class AccountExternalEx(BaseModel):
    """
    Extended Detail akun eksternal
    """
    
    isActive: bool = Field(
        default=True,
        title="Aktif",
        description="Status keaktifan akun eksternal",
        examples=[
            True
        ]
    )

# --------------------------------------------------------------------------

class AccountExternalCreateRequestBase(AccountExternalDetail):
    username: str | None = Field(
        default=None,
        title="Nama Akun",
        description="Nama akun. Jika `null` akan dibuatkan secara otomatis",
        examples=[
            "taufik"
        ]
    )
    email: EmailStr | None = Field(
        default=None,
        title="Email",
        description="Alamat email",
        examples=[
            "example@localhost.demo"
        ]
    )
    phone: str | None = Field(
        default=None,
        title="Phone",
        description="Nomor telepon",
        examples=[
            "081226526666"
        ]
    )
    password: str | None = Field(
        default=None,
        title="Kata sandi",
        description="Kata sandi akun. Jika `null`, akun tidak dapat login",
        examples=["Pass*1234"]
    )

class AccountExternalCreateRequestParam(AccountExternalCreateRequestBase):
    """
    Parameter pembuatan akun
    """

    companyCategoryIds: List[AccountExternalCompanyCategory] = Field(
        default=...,
        title="Daftar Perusahaan",
        description="Daftar Perusahaan yang terhubung dengan akun"
    )

class AccountExternalCreateRequest(AccountExternalCreateRequestBase):
    """
    Request pembuatan akun eksternal
    """

    pass

# --------------------------------------------------------------------------

class AccountExternalUpdateRequest(AccountExternalDetail):
    username: str = Field(
        default=...,
        title="Nama Akun",
        description="Nama akun",
        examples=[
            "taufik"
        ]
    )
    email: EmailStr | None = Field(
        default=None,
        title="Email",
        description="Alamat email",
        examples=[
            "example@localhost.demo"
        ]
    )
    phone: str | None = Field(
        default=None,
        title="Phone",
        description="Nomor telepon",
        examples=[
            "081226526666"
        ]
    )

# --------------------------------------------------------------------------

class AccountExternalView(AccountExternalEx, AccountExternalIdentity, AccountExternalDetail):
    id: ObjectId = Field(
        default=...,
        alias="_id",
        title="Id Akun External",
        description="Id akun eksternal (accountExternalId)"
    )
    """
    accountExternalId
    
    Id Akun External
    """

class ResponseAccountExternalView(ResponseModel):
    data: AccountExternalView

class ResponsePaging2AccountExternalView(ResponseModel):
    data: MsPaginationResult2[AccountExternalView]

# --------------------------------------------------------------------------

class AccountExternalName(BaseModel):
    name: str = Field(
        default=...,
        title="Nama",
        description="Nama",
        examples=[
            "Taufik"
        ]
    )
    id: ObjectId = Field(
        default=...,
        alias="_id",
        title="Id Akun External",
        description="Id akun eksternal (accountExternalId)"
    )
    """
    accountExternalId
    
    Id Akun External
    """

# --------------------------------------------------------------------------

class AccountExternalSearchField(str, Enum):
    nama = "name"
    username = "username"
    email = "email"
    phone = "phone"

# --------------------------------------------------------------------------

class AccountExternalCompanyCategoryIds(BaseModel):
    name: str = Field(
        default=...,
        title="Nama",
        description="Nama",
        examples=[
            "Taufik"
        ]
    )
    companyCategoryIds: List[AccountExternalCompanyCategory] = Field(
        default=...,
        title="Daftar Perusahaan",
        description="Daftar Perusahaan yang terhubung dengan akun"
    )
    id: ObjectId = Field(
        default=...,
        alias="_id",
        title="Id Akun External",
        description="Id akun eksternal (accountExternalId)"
    )
    """
    accountExternalId
    
    Id Akun External
    """
