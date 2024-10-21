from pydantic import EmailStr, Field
from models.lead.enumLead import LeadStatus, LeadType
from models.shared.modelDataType import BaseModel, ObjectId
from models.shared.modelPagination import MsPaginationResult
from models.shared.modelResponse import ResponseModel
from models.shared.modelAuditData import AuditData

class Pic(BaseModel):
    name: str = Field(
        default=...,
        title="Name",
        examples=["SMAN 2 Dumai"]
    )
    email: EmailStr | None = Field(
        default=None,
        title="Email",
        examples=[
            "example@localhost.demo"
        ]
    )
    phone: str | None = Field(
        default=None,
        title="Phone",
        examples=[
            "081226526666"
        ]
    )


class LeadBase(BaseModel):
    name: str = Field(
        default=...,
        title="Name",
        examples=["SMAN 2 Dumai"]
    )
    email: EmailStr | None = Field(
        default=None,
        title="Email",
        examples=[
            "example@localhost.demo"
        ]
    )
    phone: str | None = Field(
        default=None,
        title="Phone",
        examples=[
            "081226526666"
        ]
    )
    requirementList: list[str] | None = Field(
        [],
        title="Requirement List",
        examples=[
            ["Kartu","LMS"]
        ]
    )
    pic: Pic | None = Field(
        default=None,
        title="PIC Data"
    )
    potentialRevenue: int = Field(
        ...,
        gt=0,
        title="Potential Revenue"
    )
    potentialSize: int = Field(
        ...,
        gt=0,
        title="Potential Size"
    )
    leadTags: list[ObjectId] | None = Field(
        default=[],
        title="Lead Tag Id"
    )
    partnerId: ObjectId | None = Field(
        default=None,
        title="Partner Id"
    )
    salesId: ObjectId | None = Field(
        default=None,
        title="Sales Id"
    ) 


class LeadEx(LeadBase):
    companyId: ObjectId = Field(
        default=...,
        title="Company Id"
    )
    masterDataId: ObjectId = Field(
        default=...,
        title="Master Data Id"
    )
    
    type: LeadType = Field(
        ...,
        title="Lead Type"
    )
    status: LeadStatus = Field(
        default=...,
        title="Lead Status",
    )

# --------------------------------------------------------------------------
class LeadInDb(AuditData, LeadEx):
    id: ObjectId = Field(
        default=...,
        alias="_id",
        title="Lead Id",
        description="Lead Id"
    )

class LeadCreateWebRequest(LeadBase):
    pass

class LeadCreateCommandRequest(AuditData, LeadEx):
    pass

# --------------------------------------------------------------------------
class LeadView(LeadEx):
    id: ObjectId = Field(
        default=...,
        alias="_id",
        title="Lead Id",
        description="Lead Id"
    )

class ResponseLeadView(ResponseModel):
    data: LeadView

class ResponsePagingLeadView(ResponseModel):
    data: MsPaginationResult[LeadView]

class ResponseComboLeadView(ResponseModel):
    data: list[LeadView]

# --------------------------------------------------------------------------
