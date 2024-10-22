from datetime import datetime, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, Path, Query

from auth.authUser import AuthUserDep
from controller.controllerGenericMaterial import GenericMaterialController
from models.generic_material.modelGenericMaterial import GenericMaterialCreateWebRequest, ResponseComboGenericMaterialView, ResponseGenericMaterialView, ResponsePagingGenericMaterialView
from models.service_membership.modelCredentialLocation import CredentialLocation
from models.service_membership.modelMembershipAuth import VerifyEndpointCompanyResult
from models.shared.modelDataType import ObjectId
from models.shared.modelPagination import MsPagination
from models.shared.modelResponse import SuccessMessage
from utils.util_http_exception import MsHTTPBadRequestException, MsHTTPNotFoundException


ApiRouter_Generic_Material = APIRouter(
    prefix="/generic_material",
    tags=["Generic Material Management"]
)

@ApiRouter_Generic_Material.get(
    path="/find",
    response_model=ResponsePagingGenericMaterialView,
    operation_id="find_generic_material",
    summary="Find Generic Material",
    openapi_extra={
        "x-credentialLocations": [
            CredentialLocation.company
        ]
    }
)
async def ApiRouter_Generic_Material_Find(
    credential: Annotated[VerifyEndpointCompanyResult, Depends(AuthUserDep.VerifyEndpointCompany)],
    paging: Annotated[MsPagination, Depends(MsPagination.QueryParam)],
    name: str = Query(
        default=None,
        description="Generic Material Name"
    ),
    categoryId: ObjectId = Query(
        None,
        description="Generic Material Category Id"
    )
):
    data = await GenericMaterialController.Find(
        name,
        categoryId,
        credential.companyId,
        paging
    )
    return ResponsePagingGenericMaterialView(type=SuccessMessage.SUCCESS_READ, data=data)

@ApiRouter_Generic_Material.get(
    path="/combo",
    response_model=ResponseComboGenericMaterialView,
    operation_id="combo_generic_material",
    summary="Combo Generic Material",
    openapi_extra={
        "x-credentialLocations": [
            CredentialLocation.company
        ]
    }  
)
async def ApiRouter_Generic_Material_Combo(
    credential: Annotated[VerifyEndpointCompanyResult, Depends(AuthUserDep.VerifyEndpointCompany)],
    name: str = Query(
        None,
        description="Category Name"
    ),
    categoryId: ObjectId = Query(
        None,
        description="Category Name"
    )
):
    data = await GenericMaterialController.Combo(
        name,categoryId, credential.companyId
    )
    return ResponseComboGenericMaterialView(type=SuccessMessage.SUCCESS_READ, data=data)

@ApiRouter_Generic_Material.get(
    "/get/{id}",
    response_model=ResponseGenericMaterialView,
    operation_id="get_generic_material_by_id",
    summary="Get Generic Material by Id",
    openapi_extra={
        "x-credentialLocations": [
            CredentialLocation.company
        ]
    }   
)
async def ApiRouter_Generic_Material_Get_By_Id(
    credential: Annotated[VerifyEndpointCompanyResult, Depends(AuthUserDep.VerifyEndpointCompany)],
    id: ObjectId = Path(
        default=...,
        description="Generic Material Id"
        )
):
    data= await GenericMaterialController.GetByIdAndCompanyId(
        id,credential.companyId
    )
    return ResponseGenericMaterialView(type=SuccessMessage.SUCCESS_READ, data=data)

@ApiRouter_Generic_Material.post(
    path="/create",
    response_model=ResponseGenericMaterialView,
    operation_id="create_generic_material",
    summary="Create Generic Material",
    openapi_extra={
        "x-credentialLocations": [
            CredentialLocation.company
        ]
    }   
)
async def ApiRouter_Generic_Material_Create(
    credential: Annotated[VerifyEndpointCompanyResult, Depends(AuthUserDep.VerifyEndpointCompany)],
    request: GenericMaterialCreateWebRequest
):
    request.name = request.name.strip()
    if len(request.name) == 0:
        raise MsHTTPBadRequestException(
            type="EMPTY_FIELD_NAME",
            message="Nama Kategori belum diisi"
        )
    newId= await GenericMaterialController.Create(
        credential.companyId,
        request,
        datetime.now(timezone.utc).replace(tzinfo=None),
        credential.accountId
    )
    ret = await GenericMaterialController.GetByIdAndCompanyId(newId, credential.companyId)

    return ResponseGenericMaterialView(type=SuccessMessage.SUCCESS_CREATED, data=ret)

@ApiRouter_Generic_Material.put(
    path="/update/{id}",
    response_model=ResponseGenericMaterialView,
    operation_id="update_generic_material",
    summary="Update Generic Material",
    openapi_extra={
        "x-credentialLocations": [
            CredentialLocation.company
        ]
    }   
)
async def ApiRouter_Generic_Material_Update(
    credential: Annotated[VerifyEndpointCompanyResult, Depends(AuthUserDep.VerifyEndpointCompany)],
    request: GenericMaterialCreateWebRequest,
    id: ObjectId = Path(
        default=...,
        description="Generic Material Id"
    )
):
    request.name = request.name.strip()
    if len(request.name) == 0:
        raise MsHTTPBadRequestException(
            type="EMPTY_FIELD_NAME",
            message="Nama Kategori belum diisi"
        )
    updatedData = await GenericMaterialController.UpdateByIdAndCompanyId(
        id,
        request,
        credential.companyId,
        datetime.now(timezone.utc).replace(tzinfo=None),
        credential.accountId
    )

    return ResponseGenericMaterialView(type=SuccessMessage.SUCCESS_UPDATED, data = updatedData)

@ApiRouter_Generic_Material.delete(
    path="/delete/{id}",
    response_model=ResponseGenericMaterialView,
    operation_id="delete_generic_material",
    summary="Delete Generic Material",
    openapi_extra={
        "x-credentialLocations": [
            CredentialLocation.company
        ]
    }
)
async def ApiRouter_Generic_Material_Delete(
    credential: Annotated[VerifyEndpointCompanyResult, Depends(AuthUserDep.VerifyEndpointCompany)],
    id: ObjectId = Path(
        default=...,
        description="Generic Material Id"
    )
):
    updatedData = await GenericMaterialController.Delete(
        id,
        credential.companyId,
        datetime.now(timezone.utc).replace(tzinfo=None),
        credential.accountId
    )
    if updatedData is None:
        raise MsHTTPNotFoundException("GENERIC_MATERIAL_NOT_FOUND", "Generic Material not found")
    
    return ResponseGenericMaterialView(type=SuccessMessage.SUCCESS_DELETED, data = updatedData)