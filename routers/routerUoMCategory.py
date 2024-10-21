from datetime import datetime, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, Path, Query

from auth.authUser import AuthUserDep
from controller.controllerUoMCategory import UoMCategoryController
from models.service_membership.modelCredentialLocation import CredentialLocation
from models.service_membership.modelMembershipAuth import VerifyEndpointCompanyResult
from models.shared.modelDataType import ObjectId
from models.shared.modelPagination import MsPagination
from models.shared.modelResponse import SuccessMessage
from models.uom.modelUoMCategory import ResponseComboUoMCategoryView, ResponsePagingUoMCategoryView, ResponseUoMCategoryView, UoMCategoryCreateWebRequest
from utils.util_http_exception import MsHTTPBadRequestException, MsHTTPNotFoundException

ApiRouter_UoM_Category = APIRouter(
    prefix="/uom/category",
    tags=["UoM Category Management"]
)

@ApiRouter_UoM_Category.get(
    path="/find",
    response_model=ResponsePagingUoMCategoryView,
    operation_id="find_uom_category",
    summary="Find Unit Of Measure Category",
    openapi_extra={
        "x-credentialLocations": [
            CredentialLocation.company
        ]
    }
)
async def ApiRouter_UoM_Category_Find(
    credential: Annotated[VerifyEndpointCompanyResult, Depends(AuthUserDep.VerifyEndpointCompany)],
    paging: Annotated[MsPagination, Depends(MsPagination.QueryParam)],
    name: str = Query(
        default=None,
        description="Unit Of Measure Category Name"
    )
):
    data = await UoMCategoryController.Find(
        name,
        credential.companyId,
        paging
    )
    return ResponsePagingUoMCategoryView(type=SuccessMessage.SUCCESS_READ, data=data)

@ApiRouter_UoM_Category.get(
    path="/combo",
    response_model=ResponseComboUoMCategoryView,
    operation_id="combo_uom_category",
    summary="Combo Unit Of Measure Category",
    openapi_extra={
        "x-credentialLocations": [
            CredentialLocation.company
        ]
    }  
)
async def ApiRouter_UoM_Category_Combo(
    credential: Annotated[VerifyEndpointCompanyResult, Depends(AuthUserDep.VerifyEndpointCompany)],
    name: str = Query(
        None,
        description="Category Name"
    )
):
    data = await UoMCategoryController.Combo(
        name, credential.companyId
    )
    return ResponseComboUoMCategoryView(type=SuccessMessage.SUCCESS_READ, data=data)

@ApiRouter_UoM_Category.get(
    "/get/{id}",
    response_model=ResponseUoMCategoryView,
    operation_id="get_uom_category_by_id",
    summary="Get Unit Of Measure Category by Id",
    openapi_extra={
        "x-credentialLocations": [
            CredentialLocation.company
        ]
    }   
)
async def ApiRouter_UoM_Category_Get_By_Id(
    credential: Annotated[VerifyEndpointCompanyResult, Depends(AuthUserDep.VerifyEndpointCompany)],
    id: ObjectId = Path(
        default=...,
        description="UoM Category Id"
        )
):
    data= await UoMCategoryController.GetByIdAndCompanyId(
        id,credential.companyId
    )

    return ResponseUoMCategoryView(type=SuccessMessage.SUCCESS_READ, data=data)

@ApiRouter_UoM_Category.post(
    path="/create",
    response_model=ResponseUoMCategoryView,
    operation_id="create_uom_category",
    summary="Create Unit Of Measure Category",
    openapi_extra={
        "x-credentialLocations": [
            CredentialLocation.company
        ]
    }   
)
async def ApiRouter_UoM_Category_Create(
    credential: Annotated[VerifyEndpointCompanyResult, Depends(AuthUserDep.VerifyEndpointCompany)],
    request: UoMCategoryCreateWebRequest
):
    request.name = request.name.strip()
    if len(request.name) == 0:
        raise MsHTTPBadRequestException(
            type="EMPTY_FIELD_NAME",
            message="Nama Kategori belum diisi"
        )
    newCategory= await UoMCategoryController.Create(
        credential.companyId,
        request,
        datetime.now(timezone.utc).replace(tzinfo=None),
        credential.accountId
    )
    ret = await UoMCategoryController.GetByIdAndCompanyId(newCategory, credential.companyId)

    return ResponseUoMCategoryView(type=SuccessMessage.SUCCESS_CREATED, data=ret)

@ApiRouter_UoM_Category.put(
    path="/update/{id}",
    response_model=ResponseUoMCategoryView,
    operation_id="update_uom_category",
    summary="Update Unit Of Measure Category",
    openapi_extra={
        "x-credentialLocations": [
            CredentialLocation.company
        ]
    }   
)
async def ApiRouter_UoM_Category_Update(
    credential: Annotated[VerifyEndpointCompanyResult, Depends(AuthUserDep.VerifyEndpointCompany)],
    request: UoMCategoryCreateWebRequest,
    id: ObjectId = Path(
        default=...,
        description="UoM Category Id"
    )
):
    request.name = request.name.strip()
    if len(request.name) == 0:
        raise MsHTTPBadRequestException(
            type="EMPTY_FIELD_NAME",
            message="Nama Kategori belum diisi"
        )
    updatedData = await UoMCategoryController.UpdateByIdAndCompanyId(
        id,
        request,
        credential.companyId,
        datetime.now(timezone.utc).replace(tzinfo=None),
        credential.accountId
    )

    return ResponseUoMCategoryView(type=SuccessMessage.SUCCESS_UPDATED, data = updatedData)

@ApiRouter_UoM_Category.delete(
    path="/delete/{id}",
    response_model=ResponseUoMCategoryView,
    operation_id="delete_uom_category",
    summary="Delete Unit Of Measure Category",
    openapi_extra={
        "x-credentialLocations": [
            CredentialLocation.company
        ]
    }
)
async def ApiRouter_UoM_Category_Delete(
    credential: Annotated[VerifyEndpointCompanyResult, Depends(AuthUserDep.VerifyEndpointCompany)],
    id: ObjectId = Path(
        default=...,
        description="UoM Category Id"
    )
):
    updatedData = await UoMCategoryController.Delete(
        id,
        credential.companyId,
        datetime.now(timezone.utc).replace(tzinfo=None),
        credential.accountId
    )
    if updatedData is None:
        raise MsHTTPNotFoundException("UOM_CATEGORY_FOUND", "Unit Of Measure Category not found")
    
    return ResponseUoMCategoryView(type=SuccessMessage.SUCCESS_DELETED, data = updatedData)