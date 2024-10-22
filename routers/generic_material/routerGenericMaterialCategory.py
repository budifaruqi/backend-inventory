from datetime import datetime, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, Path, Query

from auth.authUser import AuthUserDep
from controller.controllerGenericMaterialCategory import GenericMaterialCategoryController
from models.generic_material.modelGenericMaterialCategory import GenericMaterialCategoryCreateWebRequest, ResponseComboGenericMaterialCategoryView, ResponseGenericMaterialCategoryView, ResponsePagingGenericMaterialCategoryView
from models.service_membership.modelCredentialLocation import CredentialLocation
from models.service_membership.modelMembershipAuth import VerifyEndpointCompanyResult
from models.shared.modelDataType import ObjectId
from models.shared.modelPagination import MsPagination
from models.shared.modelResponse import SuccessMessage
from utils.util_http_exception import MsHTTPBadRequestException, MsHTTPNotFoundException


ApiRouter_Generic_Material_Category = APIRouter(
    prefix="/generic_material/category",
    tags=["Generic Material Category Management"]
)

@ApiRouter_Generic_Material_Category.get(
    path="/find",
    response_model=ResponsePagingGenericMaterialCategoryView,
    operation_id="find_generic_material_category",
    summary="Find Generic Material Category",
    openapi_extra={
        "x-credentialLocations": [
            CredentialLocation.company
        ]
    }
)
async def ApiRouter_Generic_Material_Category_Find(
    credential: Annotated[VerifyEndpointCompanyResult, Depends(AuthUserDep.VerifyEndpointCompany)],
    paging: Annotated[MsPagination, Depends(MsPagination.QueryParam)],
    name: str = Query(
        default=None,
        description="Generic Material Category Name"
    )
):
    data = await GenericMaterialCategoryController.Find(
        name,
        credential.companyId,
        paging
    )
    return ResponsePagingGenericMaterialCategoryView(type=SuccessMessage.SUCCESS_READ, data=data)

@ApiRouter_Generic_Material_Category.get(
    path="/combo",
    response_model=ResponseComboGenericMaterialCategoryView,
    operation_id="combo_generic_material_category",
    summary="Combo Generic Material Category",
    openapi_extra={
        "x-credentialLocations": [
            CredentialLocation.company
        ]
    }  
)
async def ApiRouter_Generic_Material_Category_Combo(
    credential: Annotated[VerifyEndpointCompanyResult, Depends(AuthUserDep.VerifyEndpointCompany)],
    name: str = Query(
        None,
        description="Category Name"
    )
):
    data = await GenericMaterialCategoryController.Combo(
        name, credential.companyId
    )
    return ResponseComboGenericMaterialCategoryView(type=SuccessMessage.SUCCESS_READ, data=data)

@ApiRouter_Generic_Material_Category.get(
    "/get/{id}",
    response_model=ResponseGenericMaterialCategoryView,
    operation_id="get_generic_material_category_by_id",
    summary="Get Generic Material Category by Id",
    openapi_extra={
        "x-credentialLocations": [
            CredentialLocation.company
        ]
    }   
)
async def ApiRouter_Generic_Material_Category_Get_By_Id(
    credential: Annotated[VerifyEndpointCompanyResult, Depends(AuthUserDep.VerifyEndpointCompany)],
    id: ObjectId = Path(
        default=...,
        description="Generic Material Category Id"
        )
):
    data= await GenericMaterialCategoryController.GetByIdAndCompanyId(
        id,credential.companyId
    )

    return ResponseGenericMaterialCategoryView(type=SuccessMessage.SUCCESS_READ, data=data)

@ApiRouter_Generic_Material_Category.post(
    path="/create",
    response_model=ResponseGenericMaterialCategoryView,
    operation_id="create_generic_material_category",
    summary="Create Generic Material Category",
    openapi_extra={
        "x-credentialLocations": [
            CredentialLocation.company
        ]
    }   
)
async def ApiRouter_Generic_Material_Category_Create(
    credential: Annotated[VerifyEndpointCompanyResult, Depends(AuthUserDep.VerifyEndpointCompany)],
    request: GenericMaterialCategoryCreateWebRequest
):
    request.name = request.name.strip()
    if len(request.name) == 0:
        raise MsHTTPBadRequestException(
            type="EMPTY_FIELD_NAME",
            message="Nama Kategori belum diisi"
        )
    newCategory= await GenericMaterialCategoryController.Create(
        credential.companyId,
        request,
        datetime.now(timezone.utc).replace(tzinfo=None),
        credential.accountId
    )
    ret = await GenericMaterialCategoryController.GetByIdAndCompanyId(newCategory, credential.companyId)

    return ResponseGenericMaterialCategoryView(type=SuccessMessage.SUCCESS_CREATED, data=ret)

@ApiRouter_Generic_Material_Category.put(
    path="/update/{id}",
    response_model=ResponseGenericMaterialCategoryView,
    operation_id="update_generic_material_category",
    summary="Update Generic Material Category",
    openapi_extra={
        "x-credentialLocations": [
            CredentialLocation.company
        ]
    }   
)
async def ApiRouter_Generic_Material_Category_Update(
    credential: Annotated[VerifyEndpointCompanyResult, Depends(AuthUserDep.VerifyEndpointCompany)],
    request: GenericMaterialCategoryCreateWebRequest,
    id: ObjectId = Path(
        default=...,
        description="Generic Material Category Id"
    )
):
    request.name = request.name.strip()
    if len(request.name) == 0:
        raise MsHTTPBadRequestException(
            type="EMPTY_FIELD_NAME",
            message="Nama Kategori belum diisi"
        )
    updatedData = await GenericMaterialCategoryController.UpdateByIdAndCompanyId(
        id,
        request,
        credential.companyId,
        datetime.now(timezone.utc).replace(tzinfo=None),
        credential.accountId
    )

    return ResponseGenericMaterialCategoryView(type=SuccessMessage.SUCCESS_UPDATED, data = updatedData)

@ApiRouter_Generic_Material_Category.delete(
    path="/delete/{id}",
    response_model=ResponseGenericMaterialCategoryView,
    operation_id="delete_generic_material_category",
    summary="Delete Generic Material Category",
    openapi_extra={
        "x-credentialLocations": [
            CredentialLocation.company
        ]
    }
)
async def ApiRouter_Generic_Material_Category_Delete(
    credential: Annotated[VerifyEndpointCompanyResult, Depends(AuthUserDep.VerifyEndpointCompany)],
    id: ObjectId = Path(
        default=...,
        description="Generic Material Category Id"
    )
):
    updatedData = await GenericMaterialCategoryController.Delete(
        id,
        credential.companyId,
        datetime.now(timezone.utc).replace(tzinfo=None),
        credential.accountId
    )
    if updatedData is None:
        raise MsHTTPNotFoundException("GENERIC_MATERIAL_CATEGORY_NOT_FOUND", "Generic Material Category not found")
    
    return ResponseGenericMaterialCategoryView(type=SuccessMessage.SUCCESS_DELETED, data = updatedData)