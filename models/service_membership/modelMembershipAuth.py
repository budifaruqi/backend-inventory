from pydantic import Field

from models.service_membership.enumRoleLocation import RoleLocation
from models.shared.modelDataType import BaseModel, ObjectId
from models.shared.modelResponse import ResponseModel



class MembershipRoleClaimed(BaseModel):
    roleId: ObjectId = Field(
        default=...,
        title="Id Peran Hak Akses",
        description="Id peran hak akses"
    )
    name: str = Field(
        default=...,
        title="Nama Peran Hak Akses",
        description="Nama peran hak akses",
        examples=[
            "role_name"
        ]
    )
    location: RoleLocation = Field(
        default=...,
        title="Lokasi Peran Hak Akses",
        description="Lokasi peran hak akses",
        examples=[RoleLocation.company]
    )

# ==========================================================================

class VerifyEndpointBase(BaseModel):
    accountId: ObjectId = Field(
        default=...,
        title="Id AKun",
        description="Id akun"
    )
    roleClaimed: list[MembershipRoleClaimed] = Field(
        default=...,
        description="Peran hak akses yang dimiliki pada kredensial akun"
    )
    roleName: str | None = Field(
        default=None,
        description="Nama peran hak akses yang disetujui, jika `null` berarti endpoint bersangkutan menggunakan mode `allow_all`"
    )

# ==========================================================================

class VerifyEndpointServiceResult(VerifyEndpointBase):
    companyCategoryId: ObjectId | None = Field(
        default=...,
        title="Id Kategori Perusahaan",
        description="Id kategori perusahaan (jika `null`, berarti lokasi kredensial di sistem)"
    )
    companyId: ObjectId | None = Field(
        default=...,
        title="Id Perusahaan",
        description="Id perusahaan (jika `null`, berarti lokasi kredensial di sistem)"
    )
    roleLocation: RoleLocation = Field(
        default=...,
        description="Lokasi peran hak akses yang disetujui"
    )

class ResponsVerifyEndpointServiceResult(ResponseModel):
    data: VerifyEndpointServiceResult

# ==========================================================================

class VerifyEndpointCompanyResult(VerifyEndpointBase):
    companyCategoryId: ObjectId = Field(
        default=...,
        title="Id Kategori Perusahaan",
        description="Id kategori perusahaan (jika `null`, berarti lokasi kredensial di sistem)"
    )
    companyId: ObjectId = Field(
        default=...,
        title="Id Perusahaan",
        description="Id perusahaan (jika `null`, berarti lokasi kredensial di sistem)"
    )

class ResponsVerifyEndpointCompanyResult(ResponseModel):
    data: VerifyEndpointCompanyResult

# ==========================================================================

class VerifyEndpointSystemResult(VerifyEndpointBase):
    pass

# ==========================================================================
