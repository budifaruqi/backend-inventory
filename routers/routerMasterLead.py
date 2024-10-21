from typing import Annotated
from fastapi import APIRouter, Depends, Path, Query

from auth.authUser import AuthUserDep
from controller.controllerMasterLead import MasterLeadController
from models.lead.enumLead import LeadStatus, LeadType
from models.lead.modelLead import LeadCreateWebRequest, ResponseComboLeadView, ResponseLeadView, ResponsePagingLeadView
from models.service_membership.modelCredentialLocation import CredentialLocation
from models.service_membership.modelMembershipAuth import VerifyEndpointCompanyResult
from models.shared.modelDataType import ObjectId
from models.shared.modelPagination import MsPagination
from models.shared.modelResponse import SuccessMessage
from utils.util_http_exception import MsHTTPBadRequestException, MsHTTPNotFoundException
from utils.validation.validationPhoneNumber import ValidatePhoneNumber


ApiRouter_Master_Generic_Material = APIRouter(
    prefix="/master/lead",
    tags=["Master Lead Management"]
)

@ApiRouter_Master_Generic_Material.get(
    path="/find/{masterDataId}",
    response_model=ResponsePagingLeadView,
    operation_id="find_master_lead",
    summary="Find Master Lead",
    openapi_extra={
        "x-credentialLocations": [
            CredentialLocation.company
        ]
    }     
)
async def ApiRouter_Master_Lead_Find(
    credential: Annotated[VerifyEndpointCompanyResult, Depends(AuthUserDep.VerifyEndpointCompany)],
    paging: Annotated[MsPagination, Depends(MsPagination.QueryParam)],
    masterDataId: ObjectId = Path(
        default=...,
        description="Master Data Id"
    ),
    name: str = Query(
        None,
        description="Lead Name"
        ),
    type: LeadType = Query(
        None,
        description="Lead Type"
    ),
    partnerId: ObjectId = Query(
        None,
        description="Partner Id"
    ),
    status: LeadStatus = Query(
        None,
        description="Lead Status"
    ) ,
    tags: list[str] = Query(
        None,
        description="Lead Tags"
    )
) :
    data = await MasterLeadController.Find(
        masterDataId,
        name,
        type,
        partnerId,
        status,
        tags,
        credential.companyId,
        paging
    )
    return ResponsePagingLeadView(type=SuccessMessage.SUCCESS_READ, data=data)

@ApiRouter_Master_Generic_Material.get(
    "/combo/{masterDataId}",
    response_model=ResponseComboLeadView,
    operation_id="combo_master_lead",
    summary="Combo Master Lead",
    openapi_extra={
        "x-credentialLocations": [
            CredentialLocation.company
        ]
    }   
)
async def ApiRouter_Master_Lead_Combo(
    credential: Annotated[VerifyEndpointCompanyResult, Depends(AuthUserDep.VerifyEndpointCompany)],
    masterDataId: ObjectId = Path(
        default=...,
        description="Master Data Id"
    ),
    name: str = Query(
        None,
        description="Lead Name"
        ),
    type: LeadType = Query(
        None,
        description="Lead Type"
    ),
    partnerId: ObjectId = Query(
        None,
        description="Partner Id"
    ),
    status: LeadStatus = Query(
        None,
        description="Lead Status"
    ) ,
    tags: list[str] = Query(
        None,
        description="Lead Tags"
    )
) :
    data = await MasterLeadController.Combo(
        masterDataId,
        name,
        type,
        partnerId,
        status,
        tags,
        credential.companyId
    )
    return ResponseComboLeadView(type=SuccessMessage.SUCCESS_READ, data=data)


@ApiRouter_Master_Generic_Material.get(
    path="/get/{masterDataId}/{id}",
    response_model=ResponseLeadView,
    operation_id="find_master_lead_by_id",
    summary="Find Master Lead By Id",
    openapi_extra={
        "x-credentialLocations": [
            CredentialLocation.company
        ]
    }     
)
async def ApiRouter_Master_Lead_Get_By_id(
    credential: Annotated[VerifyEndpointCompanyResult, Depends(AuthUserDep.VerifyEndpointCompany)],
    id: ObjectId = Path(
        default=...,
        description="Lead Id"
        ),
    masterDataId: ObjectId = Path(
        default=...,
        description="Master Data Id"
    )
):
    data = await MasterLeadController.GetByIdAndMasterDataId(
        id,
        credential.companyId,
        masterDataId
    )

    return ResponseLeadView(type=SuccessMessage.SUCCESS_READ, data=data)

@ApiRouter_Master_Generic_Material.post(
    path="/create/{masterDataId}",
    response_model=ResponseLeadView,
    operation_id="create_master_lead",
    summary="Create Master Lead",
    openapi_extra={
        "x-credentialLocations": [
            CredentialLocation.company
        ]
    }     
)
async def ApiRouter_Master_Lead_Create(
    credential: Annotated[VerifyEndpointCompanyResult, Depends(AuthUserDep.VerifyEndpointCompany)],
    request: LeadCreateWebRequest,
    masterDataId: ObjectId = Path(
        default=...,
        description="Master Data Id"
    )
):
    request.name = request.name.strip()
    if len(request.name) == 0:
        raise MsHTTPBadRequestException(
            type="EMPTY_FIELD_NAME",
            message="Nama Lead belum diisi"
        )
    print(request.phone)
    if request.phone != None:
        request.phone = ValidatePhoneNumber(request.phone)
    if request.pic != None and request.pic.phone != None:
        request.pic.phone = ValidatePhoneNumber(request.pic.phone)
    print(request.phone)

    newLead = await MasterLeadController.Create(
        credential.companyId,
        masterDataId,
        request,
        credential.accountId
    )

    return ResponseLeadView(type=SuccessMessage.SUCCESS_CREATED, data=newLead)

@ApiRouter_Master_Generic_Material.put(
    path="/update/{masterDataId}/{id}",
    response_model=ResponseLeadView,
    operation_id="update_master_lead",
    summary="Update Master Lead",
    openapi_extra={
        "x-credentialLocations": [
            CredentialLocation.company
        ]
    }  
)
async def ApiRouter_Master_Lead_Update(
    credential: Annotated[VerifyEndpointCompanyResult, Depends(AuthUserDep.VerifyEndpointCompany)],
    request: LeadCreateWebRequest,
    id: ObjectId = Path(
        default=...,
        description="Lead Id"
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
            message="Nama Lead belum diisi"
        )
    print(request.phone)
    if request.phone != None:
        request.phone = ValidatePhoneNumber(request.phone)
    if request.pic != None and request.pic.phone != None:
        request.pic.phone = ValidatePhoneNumber(request.pic.phone)
    print(request.phone)

    newLead = await MasterLeadController.Update(
        id,
        credential.companyId,
        masterDataId,
        request,
        credential.accountId
    )

    return ResponseLeadView(type=SuccessMessage.SUCCESS_UPDATED, data=newLead)

@ApiRouter_Master_Generic_Material.delete(
    path="/delete/{masterDataId}/{id}",
    response_model=ResponseLeadView,
    operation_id="delete_master_lead",
    summary="Delete Master Lead",
    openapi_extra={
        "x-credentialLocations": [
            CredentialLocation.company
        ]
    } 
)
async def ApiRouter_Master_Lead_Delete(
    credential: Annotated[VerifyEndpointCompanyResult, Depends(AuthUserDep.VerifyEndpointCompany)],
    id: ObjectId = Path(
        default=...,
        description="Lead Id"
        ),
    masterDataId: ObjectId = Path(
        default=...,
        description="Master Data Id"
    )
): 
    data = await MasterLeadController.Delete(
        id,
        credential.companyId,
        masterDataId,
        credential.accountId
    )
    if data is None:
        raise MsHTTPNotFoundException("LEAD_NOT_FOUND", "Lead not found")
    
    return ResponseLeadView(type=SuccessMessage.SUCCESS_DELETED, data=data)
    