
from typing import Annotated
from fastapi import APIRouter, Body, Depends, Path, Query

from auth.authUser import AuthUserDep
from controller.controllerMasterDataFollower import MasterDataFollowerController
from models.master_data_follower.enumMasterData import MasterDataFollowerStatus
from models.master_data_follower.modelMasterDataFollower import MasterDataFollowerApproveRequest, ResponseMasterDataFollowerView, ResponsePagingMasterDataFollowerView
from models.service_membership.modelCredentialLocation import CredentialLocation
from models.service_membership.modelMembershipAuth import VerifyEndpointCompanyResult
from models.shared.modelDataType import ObjectId
from models.shared.modelPagination import MsPagination
from models.shared.modelResponse import SuccessMessage
from models.shared.modelSample import SampleModel


ApiRouter_Master_Data_Follower = APIRouter(
    prefix="/master_data_follower",
    tags=["Master Data Follower Management"]
)

@ApiRouter_Master_Data_Follower.get(
    path="/find",
    response_model=ResponsePagingMasterDataFollowerView,
    operation_id="find_master_data_follower",
    summary="Find Master Data Follower",
    openapi_extra={
        "x-credentialLocations": [
            CredentialLocation.company
        ]
    }   
)
async def ApiRouter_Master_Data_Follower_Find(
    credential: Annotated[VerifyEndpointCompanyResult, Depends(AuthUserDep.VerifyEndpointCompany)],
    paging: Annotated[MsPagination, Depends(MsPagination.QueryParam)],
    masterDataId: ObjectId = Query(
        default=...,
        description="Master Data Id"
    ),
    companyId: ObjectId = Query(
        default=None,
        description="Follower Company Id"
    ),
    status: MasterDataFollowerStatus = Query(
        None,
        description="Master Data Follower Status"
    )
):

    data = await MasterDataFollowerController.Find(
        masterDataId = masterDataId,
        status = status,
        companyId = companyId,
        paging = paging
    )
    return ResponsePagingMasterDataFollowerView(type=SuccessMessage.SUCCESS_READ, data=data)

@ApiRouter_Master_Data_Follower.post(
    "/request/{masterDataId}",
    response_model= ResponseMasterDataFollowerView,
    operation_id="request_master_data",
    summary="Request Master Data",
    openapi_extra={
        "x-credentialLocations": [
            CredentialLocation.company
        ]
    }  
)
async def ApiRouter_Master_Data_Follower_Request(
    credential: Annotated[VerifyEndpointCompanyResult, Depends(AuthUserDep.VerifyEndpointCompany)],
    masterDataId:ObjectId = Path(
        ...,
        description="Master Data Id",
        example=SampleModel.objectId_0
    )
):
    data = await MasterDataFollowerController.Create(
        credential.companyId,
        masterDataId,
        credential.accountId)

    ret= await MasterDataFollowerController.GetByIdAndCompanyId(data, credential.companyId)

    return ResponseMasterDataFollowerView(type = SuccessMessage.SUCCESS_CREATED, data=ret)

@ApiRouter_Master_Data_Follower.patch(
    "/approve/{id}",
    response_model=ResponseMasterDataFollowerView,
    operation_id="approve_master_data_follower",
    summary="Approve Master Data Follower",
    openapi_extra={
        "x-credentialLocations": [
            CredentialLocation.company
        ]
    }   
)
async def ApiRouter_Master_Data_Follower_Approve(
    credential: Annotated[VerifyEndpointCompanyResult, Depends(AuthUserDep.VerifyEndpointCompany)],
    id: ObjectId = Path(
        ...,
        description="Master Data Follower Id",
        example=SampleModel.objectId_0
    )
):
    data = await MasterDataFollowerController.UpdateStatusById(
        credential.companyId,
        id,
        MasterDataFollowerStatus.APPROVE,
        credential.accountId
    )

    return ResponseMasterDataFollowerView(type=SuccessMessage.SUCCESS_UPDATED, data = data)

@ApiRouter_Master_Data_Follower.patch(
    "/update_config/{id}",
    response_model=ResponseMasterDataFollowerView,
    operation_id="update_config_master_data_follower",
    summary="Update Config Master Data Follower",
    openapi_extra={
        "x-credentialLocations": [
            CredentialLocation.company
        ]
    }   
)
async def ApiRouter_Master_Data_Follower_Update_Config(
    credential: Annotated[VerifyEndpointCompanyResult, Depends(AuthUserDep.VerifyEndpointCompany)],
    id: ObjectId = Path(
        ...,
        description="Master Data Follower Id",
        example=SampleModel.objectId_0
    ),
    config: MasterDataFollowerApproveRequest = Body(...)

):
    data = await MasterDataFollowerController.UpdateConfigById(
        credential.companyId,
        id,
        config,
        credential.accountId
    )

    return ResponseMasterDataFollowerView(type=SuccessMessage.SUCCESS_UPDATED, data = data)