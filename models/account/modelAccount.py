from enum import Enum
from typing import List
from pydantic import EmailStr, Field
from models.account.modelAccountCompany import AccountCompany
from models.shared.modelDataType import BaseModel, ObjectId
from models.shared.modelPagination import MsPaginationResult2
from models.shared.modelResponse import ResponseModel
from models.shared.modelSample import SampleModel


class AccountDetail(BaseModel):
    """
    Detail akun
    """

    name: str = Field(
        default=...,
        title="Nama",
        description="Nama",
        examples=[
            "Taufik"
        ]
    )
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
    
class AccountPrivilege(BaseModel):
    """
    Hak akses akun
    """
    companyIds: List[AccountCompany] = Field(
        default=...,
        title="Daftar Perusahaan",
        description="Daftar Perusahaan yang terhubung dengan akun"
    )
    roles: List[ObjectId] = Field(
        default=...,
        title="Daftar peran hak akses",
        description="Daftar peran hak akses di lokasi sistem",
        examples=[
            SampleModel.objectId_str_2,
            SampleModel.objectId_str_3
        ]
    )

class AccountEx(BaseModel):
    """
    Extended Detail akun
    """
    
    isActive: bool = Field(
        default=True,
        title="Aktif",
        description="Status keaktifan akun",
        examples=[
            True
        ]
    )

class AccountAdditional(BaseModel):
    """
    Additional Detail akun
    """
    # place additional field in here
    # eg:
    # profileUrl: str
    pass

# --------------------------------------------------------------------------

class AccountSearchField(str, Enum):
    nama = "name"
    username = "username"
    email = "email"
    phone = "phone"

# --------------------------------------------------------------------------

class AccountView(AccountAdditional, AccountEx, AccountDetail):
    id: ObjectId = Field(
        default=...,
        alias="_id",
        title="Id Akun",
        description="Id akun (accountId)"
    )
    """
    accountId
    
    Id Akun
    """

class ResponseAccountView(ResponseModel):
    data: AccountView

class ResponsePaging2AccountView(ResponseModel):
    data: MsPaginationResult2[AccountView]

# --------------------------------------------------------------------------

class AccountPrivilegeView(AccountEx, AccountPrivilege):
    name: str = Field(
        default=...,
        title="Nama",
        description="Nama",
        examples=[
            "Taufik"
        ]
    )
    username: str = Field(
        default=...,
        title="Nama Akun",
        description="Nama akun",
        examples=[
            "taufik"
        ]
    )
    id: ObjectId = Field(
        default=...,
        alias="_id",
        title="Id Akun",
        description="Id akun (accountId)"
    )
    """
    accountId
    
    Id Akun
    """

class ResponseAccountPrivilegeView(ResponseModel):
    data: AccountPrivilegeView

# --------------------------------------------------------------------------

class AccounExtPrivilegeView(AccountEx):
    roles: List[ObjectId] = Field(
        default=...,
        title="Role",
        description="Daftar role"
    )
    id: ObjectId = Field(
        default=...,
        alias="_id",
        title="Id Akun",
        description="Id akun (accountId)"
    )
    """
    accountId
    
    Id Akun
    """
    
class ResponseAccounExtPrivilegeView(ResponseModel):
    data: AccounExtPrivilegeView

# --------------------------------------------------------------------------

class AccountName(BaseModel):
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
        title="Id Akun",
        description="Id akun (accountId)"
    )
    """
    accountId
    
    Id Akun
    """

class ResponseAccountName(ResponseModel):
    data: AccountName

class ResponseListAccountName(ResponseModel):
    data: List[AccountName]

# --------------------------------------------------------------------------

class AccountPrivilegeId(AccountPrivilege):
    id: ObjectId = Field(
        default=...,
        alias="_id",
        title="Id Akun",
        description="Id akun (accountId)"
    )
    """
    accountId
    
    Id Akun
    """

# --------------------------------------------------------------------------

class AccountRole(BaseModel):
    roles: List[ObjectId] = Field(
        default=...,
        title="Daftar peran hak akses",
        description="Daftar peran hak akses di lokasi sistem",
    )
    id: ObjectId = Field(
        default=...,
        alias="_id",
        title="Id Akun",
        description="Id akun"
    )
    """
    accountId
    
    Id Akun
    """

# --------------------------------------------------------------------------

class AccountCompanyIds(BaseModel):
    companyIds: List[AccountCompany] = Field(
        default=...,
        title="Company Ids",
        description="Daftar Perusahaan"
    )
    id: ObjectId = Field(
        default=...,
        alias="_id",
        title="Id Akun",
        description="Id akun"
    )
    """
    accountId
    
    Id Akun
    """

# --------------------------------------------------------------------------

class AccountDetailId(AccountDetail):
    id: ObjectId = Field(
        default=...,
        alias="_id",
        title="Id Akun",
        description="Id akun"
    )
    """
    accountId
    
    Id Akun
    """

class ResponseAccountDetailId(ResponseModel):
    data: AccountDetailId

# --------------------------------------------------------------------------

class AccountProfileView(AccountDetail):
    id: ObjectId = Field(
        default=...,
        alias="_id",
        title="Id Akun",
        description="Id akun"
    )
    """
    accountId
    
    Id Akun
    """

class ResponseAccountProfileView(ResponseModel):
    data: AccountProfileView

# --------------------------------------------------------------------------
