from typing import List
from pydantic import Field
from models.partner.enumPartnerType import PartnerType
from models.shared.modelDataType import BaseModel, ObjectId
from models.shared.modelPagination import MsPaginationResult
from models.shared.modelResponse import ResponseModel
from models.shared.modelAuditData import AuditData
from models.shared.modelSample import SampleModel


class PartnerBase(BaseModel):
    name: str = Field(
        default=...,
        title="Name",
        description="Partner Name",
        examples=["BNI Pusat"]
    )
    type: PartnerType = Field(
        default=...,
        title="Partner Type",
        description="PUSAT, WILAYAH, CABANG"
    )
    parentId: ObjectId | None = Field(
        default=None,
        title="Parent ID"
    )
    tags: List[str] | None = Field(
        default=[],
        title="List of Partner Tags"
    )

class PartnerDetail(PartnerBase):
    childIds: List[ObjectId] = Field(
        default=[],
        title="List of Child IDs"
    )
    masterDataId: ObjectId = Field(
        default=...,
        title="Master Data Id",
        examples=[SampleModel.objectId_str_1]
    )

class PartnerEx(BaseModel):
    companyId: ObjectId = Field(
        default=...,
        title="Company Id",
        examples=[SampleModel.objectId_str_1]
    )
    

# --------------------------------------------------------------------------
class PartnerInDb(AuditData, PartnerDetail, PartnerEx):
    id: ObjectId = Field(
        default=...,
        alias="_id",
        title="Partner ID"
    )

class PartnerCreateWebRequest(PartnerBase):
    pass

class PartnerUpdateWebRequest(BaseModel):
    name: str = Field(
        default=...,
        title="Name",
        description="Partner Name",
        examples=["BNI Pusat"]
    )
    parentId: ObjectId | None = Field(
        default=None,
        title="Parent ID"
    )
    tags: List[str] = Field(
        default=...,
        title="List of Partner Tags"
    )


class PartnerCreateCommandRequest(AuditData, PartnerEx, PartnerDetail):
    pass

# --------------------------------------------------------------------------
class PartnerView(PartnerEx, PartnerDetail):
    id: ObjectId = Field(
        default=...,
        alias="_id",
        title="Partner ID"
    )

# Response model for a single partner view
class ResponsePartnerView(ResponseModel):
    data: PartnerView

# Response model for paginated partner view
class ResponsePagingPartnerView(ResponseModel):
    data: MsPaginationResult[PartnerView]


# --------------------------------------------------------------------------

    