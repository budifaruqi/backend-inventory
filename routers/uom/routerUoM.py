from datetime import datetime, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, Path, Query

from auth.authUser import AuthUserDep
from controller.controllerUoM import UoMController
from models.service_membership.modelCredentialLocation import CredentialLocation
from models.service_membership.modelMembershipAuth import VerifyEndpointCompanyResult
from models.shared.modelDataType import ObjectId
from models.shared.modelPagination import MsPagination
from models.shared.modelResponse import SuccessMessage
from models.uom.modelUoM import ResponseComboUoMView, ResponsePagingUoMView, ResponseUoMView, UoMCreateWebRequest
from utils.util_http_exception import MsHTTPBadRequestException, MsHTTPNotFoundException


ApiRouter_UoM = APIRouter(
    prefix="/uom",
    tags=["Unit Of Measure Management"]
)

@ApiRouter_UoM.get(
    path="/find",
    response_model=ResponsePagingUoMView,
    operation_id="find_uom",
    summary="Find Unit Of Measure",
    openapi_extra={
        "x-credentialLocations": [
            CredentialLocation.company
        ]
    }
)
async def ApiRouter_UoM_Find(
    credential: Annotated[VerifyEndpointCompanyResult, Depends(AuthUserDep.VerifyEndpointCompany)],
    paging: Annotated[MsPagination, Depends(MsPagination.QueryParam)],
    name: str = Query(
        default=None,
        description="Unit Of Measure Name"
    ),
    categoryId: ObjectId = Query( 
        None,
        description="Unit Of Measure Category Id"
    ),
    isActive: bool = Query(
        None,
        description="Active"
    )
):
    data = await UoMController.Find(
        name,
        categoryId,
        isActive,
        credential.companyId,
        paging
    )
    return ResponsePagingUoMView(type=SuccessMessage.SUCCESS_READ, data=data)

@ApiRouter_UoM.get(
    path="/combo",
    response_model=ResponseComboUoMView,
    operation_id="combo_uom",
    summary="Combo Unit Of Measure",
    openapi_extra={
        "x-credentialLocations": [
            CredentialLocation.company
        ]
    }  
)
async def ApiRouter_UoM_Combo(
    credential: Annotated[VerifyEndpointCompanyResult, Depends(AuthUserDep.VerifyEndpointCompany)],
    name: str = Query(
        default=None,
        description="Unit Of Measure Name"
    ),
    categoryId: ObjectId = Query( 
        None,
        description="Unit Of Measure Category Id"
    ),
    isActive: bool = Query(
        None,
        description="Active"
    )
):
    data = await UoMController.Combo(
        name, categoryId, isActive, credential.companyId
    )
    return ResponseComboUoMView(type=SuccessMessage.SUCCESS_READ, data=data)

@ApiRouter_UoM.get(
    "/get/{id}",
    response_model=ResponseUoMView,
    operation_id="get_uom_by_id",
    summary="Get Unit Of Measure by Id",
    openapi_extra={
        "x-credentialLocations": [
            CredentialLocation.company
        ]
    }   
)
async def ApiRouter_UoM_Get_By_Id(
    credential: Annotated[VerifyEndpointCompanyResult, Depends(AuthUserDep.VerifyEndpointCompany)],
    id: ObjectId = Path(
        default=...,
        description="UoM Id"
        )
):
    data= await UoMController.GetByIdAndCompanyId(
        id,credential.companyId
    )

    return ResponseUoMView(type=SuccessMessage.SUCCESS_READ, data=data)

@ApiRouter_UoM.post(
    path="/create",
    response_model=ResponseUoMView,
    operation_id="create_uom",
    summary="Create Unit Of Measure ",
    openapi_extra={
        "x-credentialLocations": [
            CredentialLocation.company
        ]
    }   
)
async def ApiRouter_UoM_Create(
    credential: Annotated[VerifyEndpointCompanyResult, Depends(AuthUserDep.VerifyEndpointCompany)],
    request: UoMCreateWebRequest
):
    request.name = request.name.strip()
    if len(request.name) == 0:
        raise MsHTTPBadRequestException(
            type="EMPTY_FIELD_NAME",
            message="Nama belum diisi"
        )
    new= await UoMController.Create(
        credential.companyId,
        request,
        datetime.now(timezone.utc).replace(tzinfo=None),
        credential.accountId
    )
    ret = await UoMController.GetByIdAndCompanyId(new, credential.companyId)

    return ResponseUoMView(type=SuccessMessage.SUCCESS_CREATED, data=ret)

@ApiRouter_UoM.put(
    path="/update/{id}",
    response_model=ResponseUoMView,
    operation_id="update_uom",
    summary="Update Unit Of Measure ",
    openapi_extra={
        "x-credentialLocations": [
            CredentialLocation.company
        ]
    }   
)
async def ApiRouter_UoM_Update(
    credential: Annotated[VerifyEndpointCompanyResult, Depends(AuthUserDep.VerifyEndpointCompany)],
    request: UoMCreateWebRequest,
    id: ObjectId = Path(
        default=...,
        description="UoM  Id"
    )
):
    request.name = request.name.strip()
    if len(request.name) == 0:
        raise MsHTTPBadRequestException(
            type="EMPTY_FIELD_NAME",
            message="Nama belum diisi"
        )
    updatedData = await UoMController.UpdateByIdAndCompanyId(
        id,
        request,
        credential.companyId,
        datetime.now(timezone.utc).replace(tzinfo=None),
        credential.accountId
    )

    return ResponseUoMView(type=SuccessMessage.SUCCESS_UPDATED, data = updatedData)

@ApiRouter_UoM.delete(
    path="/delete/{id}",
    response_model=ResponseUoMView,
    operation_id="delete_uom",
    summary="Delete Unit Of Measure ",
    openapi_extra={
        "x-credentialLocations": [
            CredentialLocation.company
        ]
    }
)
async def ApiRouter_UoM_Delete(
    credential: Annotated[VerifyEndpointCompanyResult, Depends(AuthUserDep.VerifyEndpointCompany)],
    id: ObjectId = Path(
        default=...,
        description="UoM  Id"
    )
):
    updatedData = await UoMController.Delete(
        id,
        credential.companyId,
        datetime.now(timezone.utc).replace(tzinfo=None),
        credential.accountId
    )
    if updatedData is None:
        raise MsHTTPNotFoundException("UOM_NOT_FOUND", "Unit Of Measure not found")
    
    return ResponseUoMView(type=SuccessMessage.SUCCESS_DELETED, data = updatedData)
