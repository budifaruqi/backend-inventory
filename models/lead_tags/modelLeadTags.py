from pydantic import Field
from models.shared.modelDataType import BaseModel, ObjectId
from models.shared.modelPagination import MsPaginationResult
from models.shared.modelResponse import ResponseModel
from models.shared.modelAuditData import AuditData
from models.shared.modelSample import SampleModel

class LeadTagBase(BaseModel):
    name: str = Field(
        default=...,
        title="Name",
        description="Tag Name",
        examples=["Sekolah"]
    )
    description: str = Field(
        default=...,
        title="Description",
        description="Tag Description",
        examples=["Sekolah"]
    )    

class LeadTagEx(LeadTagBase):
    masterDataId: ObjectId = Field(
        default=...,
        title="Master Data Id",
        description="Master Data Id",
        examples=[SampleModel.objectId_str_1]
    )
    companyId: ObjectId = Field(
        default=...,
        title="Company Id",
        description="Company Id",
        examples=[SampleModel.objectId_str_1]
    )

# --------------------------------------------------------------------------
class LeadTagInDb(AuditData, LeadTagEx):
    id: ObjectId = Field(
        default=...,
        alias="_id",
        title="Lead Tag Id",
        description="Lead Tag Id"
    )

class LeadTagCreateWebRequest(LeadTagBase):
    pass

class LeadTagCreateCommandRequest(AuditData, LeadTagEx):
    pass

# --------------------------------------------------------------------------
class LeadTagView(LeadTagEx, LeadTagBase):
    id: ObjectId = Field(
        default=...,
        alias="_id",
        title="Lead Tag Id",
        description="Lead Tag Id"
    )

class ResponseLeadTagView(ResponseModel):
    data: LeadTagView

class ResponsePagingLeadTagView(ResponseModel):
    data: MsPaginationResult[LeadTagView]

# --------------------------------------------------------------------------
