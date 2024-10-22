from datetime import datetime, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, Path, Query

from auth.authUser import AuthUserDep
from controller.controllerMasterData import MasterDataController
from models.master_data.modelMasterData import MasterDataCreateRequest, ResponseComboMasterDataView, ResponseMasterDataView, ResponsePagingMasterDataView
from models.service_membership.modelCredentialLocation import CredentialLocation
from models.service_membership.modelMembershipAuth import VerifyEndpointCompanyResult
from models.shared.modelDataType import ObjectId
from models.shared.modelPagination import MsPagination
from models.shared.modelResponse import SuccessMessage
from models.shared.modelSample import SampleModel
from utils.util_http_exception import MsHTTPBadRequestException, MsHTTPNotFoundException


ApiRouter_Master_Data = APIRouter(
    prefix="/master_data",
    tags=["Master Data Management"]
)

@ApiRouter_Master_Data.get(
    path="/find",
    response_model=ResponsePagingMasterDataView,
    operation_id="find_master_data",
    summary="Find Master Data",
    openapi_extra={
        "x-credentialLocations": [
            CredentialLocation.company
        ]
    }   
)
async def ApiRouter_Master_Data_Find(
    credential: Annotated[VerifyEndpointCompanyResult, Depends(AuthUserDep.VerifyEndpointCompany)],
    paging: Annotated[MsPagination, Depends(MsPagination.QueryParam)],
    name: str = Query(
        default=None,
        description="Master Data's Name"
    )
) -> ResponsePagingMasterDataView:
    data= await MasterDataController.Find(
        name=name,
        companyId= credential.companyId,
        paging=paging
    )
    return ResponsePagingMasterDataView(type=SuccessMessage.SUCCESS_READ, data=data)

@ApiRouter_Master_Data.get(
    path="/combo",
    response_model=ResponseComboMasterDataView,
    operation_id="combo_master_data",
    summary="Combo Master Data",
    openapi_extra={
        "x-credentialLocations": [
            CredentialLocation.company
        ]
    }   
)
async def ApiRouter_Master_Data_Combo(
    credential: Annotated[VerifyEndpointCompanyResult, Depends(AuthUserDep.VerifyEndpointCompany)],
    name: str = Query(
        default=None,
        description="Master Data's Name"
    )
):
    data= await MasterDataController.Combo(
        name=name
    )
    return ResponseComboMasterDataView(type=SuccessMessage.SUCCESS_READ, data=data)

@ApiRouter_Master_Data.get(
    path="/get/{masterDataId}",
    response_model=ResponseMasterDataView,
    operation_id="get_master_data_by_id",
    summary="Get Master Data by Id",
    openapi_extra={
        "x-credentialLocations": [
            CredentialLocation.company
        ]
    }   
)
async def ApiRouter_Master_Data_Get_By_Id(
    credential: Annotated[VerifyEndpointCompanyResult, Depends(AuthUserDep.VerifyEndpointCompany)],
    masterDataId: ObjectId = Path(
        default=...,
        description="Master Data's Id",
        example=SampleModel.objectId_0
        )
    ):
        data = await MasterDataController.GetByIdAndCompanyId(
        id=masterDataId,
        companyId= credential.companyId
        )
    
        return ResponseMasterDataView(data=data)

@ApiRouter_Master_Data.post(
    path="/create",
    response_model=ResponseMasterDataView,
    operation_id="create_master_data",
    summary="Create Master Data",
    openapi_extra={
        "x-credentialLocations": [
            CredentialLocation.company
        ]
    }   
)
async def ApiRouter_Master_Data_Create(
    credential: Annotated[VerifyEndpointCompanyResult, Depends(AuthUserDep.VerifyEndpointCompany)],
    request:MasterDataCreateRequest
    ):
        createdTime = datetime.now(timezone.utc).replace(tzinfo=None)
        createdBy = credential.accountId
        companyId= credential.companyId

        request.name = request.name.strip()
        if len(request.name) == 0:
            raise MsHTTPBadRequestException(
                type="EMPTY_FIELD_NAME",
                message="Nama Master Data belum diisi"
            )

        newMasterDataId = await MasterDataController.Create(
                request,
                companyId,
                createdTime,
                createdBy
        )
        ret = await MasterDataController.GetByIdAndCompanyId(newMasterDataId, companyId)

        return ResponseMasterDataView(type=SuccessMessage.SUCCESS_CREATED, data=ret)

@ApiRouter_Master_Data.put(
    path="/update/{masterDataId}",
    response_model=ResponseMasterDataView,
    operation_id="update_master_data_by_id",
    summary="Update Master Data by Id",
    openapi_extra={
        "x-credentialLocations": [
            CredentialLocation.company
        ]
    }   
)
async def ApiRouter_Master_Data_Put(
    credential: Annotated[VerifyEndpointCompanyResult, Depends(AuthUserDep.VerifyEndpointCompany)],
    request: MasterDataCreateRequest,
    masterDataId: ObjectId = Path(
        default=...,
        description="Master Data's Id",
        example=SampleModel.objectId_0
        ),
    ): 
        updatedTime = datetime.now(timezone.utc).replace(tzinfo=None)
        updatedBy = credential.accountId
        companyId= credential.companyId

        request.name = request.name.strip()
        if len(request.name) == 0:
            raise MsHTTPBadRequestException(
                type="EMPTY_FIELD_NAME",
                message="Nama Master Data belum diisi"
            )

        updatedData = await MasterDataController.UpdateByIdAndCompanyId(
                masterDataId,
                request,
                companyId,
                updatedTime,
                updatedBy
        )

        return ResponseMasterDataView(type=SuccessMessage.SUCCESS_CREATED, data=updatedData)

@ApiRouter_Master_Data.delete(
    path="/delete/{masterDataId}",
    response_model=ResponseMasterDataView,
    operation_id="delete_master_data_by_id",
    summary="Delete Master Data by Id",
    openapi_extra={
        "x-credentialLocations": [
            CredentialLocation.company
        ]
    }  
)
async def ApiRouter_Master_Data_Delete(
    credential: Annotated[VerifyEndpointCompanyResult, Depends(AuthUserDep.VerifyEndpointCompany)],
    masterDataId: ObjectId = Path(
        default=...,
        description="Master Data's Id",
        example=SampleModel.objectId_0
        ),
    ): 
        updatedTime = datetime.now(timezone.utc).replace(tzinfo=None)
        updatedBy = credential.accountId
        companyId= credential.companyId
    

        updatedData = await MasterDataController.Delete(
                masterDataId,
                companyId,
                updatedTime,
                updatedBy
        )
        if updatedData is None:
            raise MsHTTPNotFoundException("MASTER_DATA_NOT_FOUND", "Master Data not found")

        return ResponseMasterDataView(type=SuccessMessage.SUCCESS_DELETED, data=updatedData)
