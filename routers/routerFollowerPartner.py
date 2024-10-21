from typing import Annotated
from fastapi import APIRouter, Depends, Path, Query
from auth.authUser import AuthUserDep
from controller.controllerMasterPartner import MasterPartnerController
from models.partner.enumPartnerType import PartnerType
from models.partner.modelPartner import PartnerCreateWebRequest, PartnerUpdateWebRequest, ResponsePagingPartnerView, ResponsePartnerView
from models.service_membership.modelCredentialLocation import CredentialLocation
from models.service_membership.modelMembershipAuth import VerifyEndpointCompanyResult
from models.shared.modelDataType import ObjectId
from models.shared.modelPagination import MsPagination
from models.shared.modelResponse import SuccessMessage
from utils.util_http_exception import MsHTTPBadRequestException

ApiRouter_Follower_Partner = APIRouter(
    prefix="/follower/partner",
    tags=["Follower Partner Management"]
)

@ApiRouter_Follower_Partner.get(
    path="/find/{followerId}",
    response_model=ResponsePagingPartnerView,
    operation_id="find_follower_partner",
    summary="Find Follower Partner",
    openapi_extra={
        "x-credentialLocations": [
            CredentialLocation.company
        ]
    }     
)
async def ApiRouter_Follower_Partner_FindByConfig(
    credential: Annotated[VerifyEndpointCompanyResult, Depends(AuthUserDep.VerifyEndpointCompany)],
    paging: Annotated[MsPagination, Depends(MsPagination.QueryParam)],
    followerId: ObjectId = Path(
        default=...,
        description="Follower Data Id"
    ),
    name: str = Query(
        None,
        description="Partner Name"
        ),
    type: PartnerType = Query(
        None,
        description="Partner Type"
    ),
    parentId: ObjectId = Query(
        None,
        description="Parent Id"
    ),
    tags: list[str] = Query(
        None,
        description="Partner Tags"
    )
    ) :
        data = await MasterPartnerController.FindByConfig(
            followerId,
            name,
            type,
            parentId,
            tags,
            credential.companyId,
            paging
        )
        return ResponsePagingPartnerView(type=SuccessMessage.SUCCESS_READ, data=data)