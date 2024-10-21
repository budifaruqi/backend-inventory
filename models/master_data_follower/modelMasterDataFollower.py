from pydantic import Field
from models.master_data_follower.enumMasterData import FollowerDataConfig, MasterDataFollowerStatus, Operation
from models.shared.modelAuditData import AuditData
from models.shared.modelDataType import BaseModel, ObjectId
from models.shared.modelPagination import MsPaginationResult
from models.shared.modelResponse import ResponseModel
from models.shared.modelSample import SampleModel

class MasterDataSetting(BaseModel):
    data: FollowerDataConfig = Field(
        title="Data"
    )
    operations: list[Operation] = Field(
        [],
        title="Data Operation"
    )
default_config = [
    MasterDataSetting(data=config, operations=[])
    for config in FollowerDataConfig
]
class MasterDataFollower(BaseModel):
    companyId: ObjectId = Field(
        title="Company Id",
        description="Company Id",
        examples=[str(SampleModel.objectId_0)]
    )
    masterDataId: ObjectId = Field(
        title="Master Data Id",
        description="Master Data Id",
        examples=[str(SampleModel.objectId_0)]
    )
    status: MasterDataFollowerStatus = Field(
        default=MasterDataFollowerStatus.REQUESTED,
        title="Config Status",
        description="Config Status"
    )
    config: list[MasterDataSetting] = Field(
        default=default_config,
    )
    
class MasterDataFollowerRequest(BaseModel):
    masterDataId: ObjectId = Field(
        title="Master Data Id",
        description="Master Data Id",
        examples=[str(SampleModel.objectId_0)]
    )
    
class MasterDataFollowerApproveRequest(BaseModel):
    config: list[MasterDataSetting] = Field(
        default=default_config,
    )

class MasterDataFollowerCreateParam(AuditData, MasterDataFollower):
    pass

# ==========================================================================

class MasterDataFollowerView(MasterDataFollower):
    id: ObjectId = Field(
        default=...,
        alias="_id",
        title="Id",
        description="Id Master Data Follower",
        examples=[str(SampleModel.objectId_0)]
    )

class ResponseMasterDataFollowerView(ResponseModel):
    data: MasterDataFollowerView

class ResponsePagingMasterDataFollowerView(ResponseModel):
    data: MsPaginationResult[MasterDataFollowerView]

# ==========================================================================

