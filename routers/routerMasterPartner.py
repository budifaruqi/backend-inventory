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

ApiRouter_Master_Partner = APIRouter(
    prefix="/master/partner",
    tags=["Master Partner Management"]
)

@ApiRouter_Master_Partner.get(
    path="/find/{masterDataId}",
    response_model=ResponsePagingPartnerView,
    operation_id="find_master_partner",
    summary="Find Master Partner",
    openapi_extra={
        "x-credentialLocations": [
            CredentialLocation.company
        ]
    }     
)
async def ApiRouter_Master_Partner_Find(
    credential: Annotated[VerifyEndpointCompanyResult, Depends(AuthUserDep.VerifyEndpointCompany)],
    paging: Annotated[MsPagination, Depends(MsPagination.QueryParam)],
    masterDataId: ObjectId = Path(
        default=...,
        description="Master Data Id"
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
    data = await MasterPartnerController.Find(
        masterDataId,
        name,
        type,
        parentId,
        tags,
        credential.companyId,
        paging
    )
    return ResponsePagingPartnerView(type=SuccessMessage.SUCCESS_READ, data=data)

@ApiRouter_Master_Partner.get(
    path="/get/{masterDataId}/{id}",
    response_model=ResponsePartnerView,
    operation_id="find_master_partner_by_id",
    summary="Find Master Partner By Id",
    openapi_extra={
        "x-credentialLocations": [
            CredentialLocation.company
        ]
    }     
)
async def ApiRouter_Master_Partner_Get_By_id(
    credential: Annotated[VerifyEndpointCompanyResult, Depends(AuthUserDep.VerifyEndpointCompany)],
    id: ObjectId = Path(
        default=...,
        description="Partner Id"
        ),
    masterDataId: ObjectId = Path(
        default=...,
        description="Master Data Id"
    )
):
    data = await MasterPartnerController.GetByIdAndMasterDataId(
        id,
        credential.companyId,
        masterDataId
    )

    return ResponsePartnerView(type=SuccessMessage.SUCCESS_READ, data=data)

@ApiRouter_Master_Partner.post(
    path="/create/{masterDataId}",
    response_model=ResponsePartnerView,
    operation_id="create_master_partner",
    summary="Create Master Partner",
    openapi_extra={
        "x-credentialLocations": [
            CredentialLocation.company
        ]
    }     
)
async def ApiRouter_Master_Partner_Create(
    credential: Annotated[VerifyEndpointCompanyResult, Depends(AuthUserDep.VerifyEndpointCompany)],
    request: PartnerCreateWebRequest,
    masterDataId: ObjectId = Path(
        default=...,
        description="Master Data Id"
    )
):
    request.name = request.name.strip()
    if len(request.name) == 0:
        raise MsHTTPBadRequestException(
            type="EMPTY_FIELD_NAME",
            message="Nama Partner belum diisi"
        )
    newPartner = await MasterPartnerController.Create(
        credential.companyId,
        masterDataId,
        request,
        credential.accountId
    )

    return ResponsePartnerView(type=SuccessMessage.SUCCESS_CREATED, data=newPartner)

@ApiRouter_Master_Partner.put(
    path="/update/{masterDataId}/{id}",
    response_model=ResponsePartnerView,
    operation_id="update_master_partner_by_id",
    summary="Update Master Partner By Id",
    openapi_extra={
        "x-credentialLocations": [
            CredentialLocation.company
        ]
    }   
)
async def ApiRouter_Master_Partner_Update_By_Id(
    credential: Annotated[VerifyEndpointCompanyResult, Depends(AuthUserDep.VerifyEndpointCompany)],
    request: PartnerUpdateWebRequest,
    id: ObjectId = Path(
        default=...,
        description="Partner Id"
        ),
    masterDataId: ObjectId = Path(
        default=...,
        description="Master Data Id"
    )
):
    request.name = request.name.strip()
    if len(request.name) == 0:
        raise MsHTTPBadRequestException(
            type="EMPTY_FIELD_NAME",
            message="Nama Partner belum diisi"
        )
    updatedData = await MasterPartnerController.UpdateByIdAndCompanyIdAndMasterDataId(
        id,
        credential.companyId,
        masterDataId,
        request,
        credential.accountId
    )
    return ResponsePartnerView(type=SuccessMessage.SUCCESS_UPDATED, data=updatedData)

@ApiRouter_Master_Partner.delete(
    path="/delete/{masterDataId}/{id}",
    response_model=ResponsePartnerView,
    operation_id="delete_master_partner_by_id",
    summary="Delete Master Partner By Id",
    openapi_extra={
        "x-credentialLocations": [
            CredentialLocation.company
        ]
    }   
)
async def ApiRouter_Master_Partner_Delete_By_Id(
    credential: Annotated[VerifyEndpointCompanyResult, Depends(AuthUserDep.VerifyEndpointCompany)],
    id: ObjectId = Path(
        default=...,
        description="Partner Id"
        ),
    masterDataId: ObjectId = Path(
        default=...,
        description="Master Data Id"
    )
):
    updatedData = await MasterPartnerController.Delete(
        id,
        credential.companyId,
        masterDataId,
        credential.accountId
    )
    
    return ResponsePartnerView(type=SuccessMessage.SUCCESS_DELETED, data=updatedData)