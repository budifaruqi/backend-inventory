from typing import Annotated
from fastapi import APIRouter, Depends, Path, Query

from auth.authUser import AuthUserDep
from controller.controllerMasterLeadTag import MasterLeadTagController
from models.lead_tags.modelLeadTags import LeadTagCreateWebRequest, ResponseLeadTagView, ResponsePagingLeadTagView
from models.service_membership.modelCredentialLocation import CredentialLocation
from models.service_membership.modelMembershipAuth import VerifyEndpointCompanyResult
from models.shared.modelDataType import ObjectId
from models.shared.modelPagination import MsPagination
from models.shared.modelResponse import SuccessMessage
from utils.util_http_exception import MsHTTPBadRequestException, MsHTTPNotFoundException

ApiRouter_Master_Lead_Tag = APIRouter(
    prefix="/master/lead_tag",
    tags=["Master Lead Tag Management"]
)

@ApiRouter_Master_Lead_Tag.get(
    path="/find/{masterDataId}",
    response_model=ResponsePagingLeadTagView,
    operation_id="find_master_lead_tag",
    summary="Find Master Lead Tag",
    openapi_extra={
        "x-credentialLocations": [
            CredentialLocation.company
        ]
    }
)
async def ApiRouter_Master_Lead_Tag_Find(
    credential: Annotated[VerifyEndpointCompanyResult, Depends(AuthUserDep.VerifyEndpointCompany)],
    paging: Annotated[MsPagination, Depends(MsPagination.QueryParam)],
    masterDataId: ObjectId = Path(
        default=...,
        description="Master Data Id"
    ),
    name: str = Query(
        default=None,
        description="Lead Tag Name"
    )
):
    data = await MasterLeadTagController.Find(
        masterDataId,
        name,
        credential.companyId,
        paging
    )
    return ResponsePagingLeadTagView(type=SuccessMessage.SUCCESS_READ, data=data)

@ApiRouter_Master_Lead_Tag.get(
    "/get/{masterDataId}/{id}",
    response_model=ResponseLeadTagView,
    operation_id="get_master_lead_tag_by_id",
    summary="Get Master Lead Tag by Id",
    openapi_extra={
        "x-credentialLocations": [
            CredentialLocation.company
        ]
    }   
)
async def ApiRouter_Master_Lead_Tag_Get_By_Id(
    credential: Annotated[VerifyEndpointCompanyResult, Depends(AuthUserDep.VerifyEndpointCompany)],
    id: ObjectId = Path(
        default=...,
        description="Lead Tag Id"
        ),
    masterDataId: ObjectId = Path(
        default=...,
        description="Master Data Id"
    )
):
    data= await MasterLeadTagController.GetByIdAndMasterDataId(
        id,
        credential.companyId,
        masterDataId
    )

    return ResponseLeadTagView(type=SuccessMessage.SUCCESS_READ, data=data)

@ApiRouter_Master_Lead_Tag.post(
    path="/create/{masterDataId}",
    response_model=ResponseLeadTagView,
    operation_id="create_master_lead_tag",
    summary="Create Master Lead Tag",
    openapi_extra={
        "x-credentialLocations": [
            CredentialLocation.company
        ]
    }   
)
async def ApiRouter_Master_Lead_Tag_Create(
    credential: Annotated[VerifyEndpointCompanyResult, Depends(AuthUserDep.VerifyEndpointCompany)],
    request: LeadTagCreateWebRequest,
    masterDataId: ObjectId = Path(
        default=...,
        description="Master Data Id"
    ),
):
    request.name = request.name.strip()
    if len(request.name) == 0:
        raise MsHTTPBadRequestException(
            type="EMPTY_FIELD_NAME",
            message="Nama Lead Tag belum diisi"
        )
    newLeadTagId= await MasterLeadTagController.Create(
        credential.companyId,
        masterDataId,
        request,
        credential.accountId
    )
    ret = await MasterLeadTagController.GetByIdAndMasterDataId(newLeadTagId, credential.companyId, masterDataId)

    return ResponseLeadTagView(type=SuccessMessage.SUCCESS_CREATED, data=ret)

@ApiRouter_Master_Lead_Tag.put(
    path="/update/{masterDataId}/{id}",
    response_model=ResponseLeadTagView,
    operation_id="update_master_lead_tag",
    summary="Update Master Lead Tag",
    openapi_extra={
        "x-credentialLocations": [
            CredentialLocation.company
        ]
    }   
)
async def ApiRouter_Master_Lead_Tag_Update(
    credential: Annotated[VerifyEndpointCompanyResult, Depends(AuthUserDep.VerifyEndpointCompany)],
    request: LeadTagCreateWebRequest,
    id: ObjectId = Path(
        default=...,
        description="Lead Tag Id"
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
            message="Nama Master Data belum diisi"
        )
    updatedData = await MasterLeadTagController.UpdateByIdAndCompanyIdAndMasterDataId(
        id,
        credential.companyId,
        masterDataId,
        request,
        credential.accountId
    )

    return ResponseLeadTagView(type=SuccessMessage.SUCCESS_UPDATED, data = updatedData)

@ApiRouter_Master_Lead_Tag.delete(
    path="/delete/{masterDataId}/{id}",
    response_model=ResponseLeadTagView,
    operation_id="delete_master_lead_tag",
    summary="Delete Master Lead Tag",
    openapi_extra={
        "x-credentialLocations": [
            CredentialLocation.company
        ]
    }
)
async def ApiRouter_Master_Lead_Tag_Delete(
    credential: Annotated[VerifyEndpointCompanyResult, Depends(AuthUserDep.VerifyEndpointCompany)],
    id: ObjectId = Path(
        default=...,
        description="Lead Tag Id"
    ),
    masterDataId: ObjectId = Path(
        default=...,
        description="Master Data Id"
    )
):
    updatedData = await MasterLeadTagController.Delete(
        id,
        credential.companyId,
        masterDataId,
        credential.accountId
    )
    if updatedData is None:
        raise MsHTTPNotFoundException("LEAD_TAG_NOT_FOUND", "Lead Tag not found")
    
    return ResponseLeadTagView(type=SuccessMessage.SUCCESS_UPDATED, data = updatedData)