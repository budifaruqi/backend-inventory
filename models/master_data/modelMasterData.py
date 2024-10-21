from pydantic import Field
from models.shared.modelAuditData import AuditData
from models.shared.modelDataType import BaseModel, ObjectId
from models.shared.modelPagination import MsPaginationResult
from models.shared.modelResponse import ResponseModel
from models.shared.modelSample import SampleModel

MAX_NAME = 50

class MasterDataDetail(BaseModel):
    name: str = Field(
        default=...,
        max_length=MAX_NAME,
        title="Name",
        description="Master Data Name",
        examples=[
            "Master Data PT. TKI & PT. FTP"
        ]
    )
     
    companyId: ObjectId = Field(
        default=...,
        title="CompanyId",
        description="Company Id",
        examples=[str(SampleModel.objectId_0)]
    )

    followerCompanyIds: list[ObjectId] = Field(
        default=[],
        title="List of Follower Company Id"
    )

class MasterDataCreateRequest(BaseModel):
    name: str = Field(
        default=...,
        max_length=MAX_NAME,
        title="Name",
        description="Master Data Name",
        examples=[
            "Master Data PT. TKI & PT. FTP"
        ]
    )

class MasterDataCreateParam(AuditData, MasterDataDetail):
    pass

# ==========================================================================

class MasterDataView(MasterDataDetail):
    id: ObjectId = Field(
        default=...,
        alias="_id",
        title="Id",
        description="Id Master Data",
        examples=[str(SampleModel.objectId_0)]
    )

class ResponseMasterDataView(ResponseModel):
    data: MasterDataView

class ResponsePagingMasterDataView(ResponseModel):
    data: MsPaginationResult[MasterDataView]
    
class ResponseComboMasterDataView(ResponseModel):
    data: list[MasterDataView]
# ==========================================================================