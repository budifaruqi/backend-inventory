from typing import Annotated
from fastapi import APIRouter, Depends

from auth.authUser import AuthUserDep
from models.service_membership.modelCredentialLocation import CredentialLocation
from models.service_membership.modelMembershipAuth import ResponsVerifyEndpointCompanyResult, VerifyEndpointCompanyResult


ApiRouter_Manage_Client = APIRouter(
    prefix="/manage_client",
    tags=["Manajemen Klien"]
)

@ApiRouter_Manage_Client.get(
    path="/test",
    response_model=ResponsVerifyEndpointCompanyResult,
    openapi_extra={
        "x-credentialLocations": [
            CredentialLocation.company
        ]
    }
)
async def ApiRouter_Manage_Client_Test(
    credential: Annotated[VerifyEndpointCompanyResult, Depends(AuthUserDep.VerifyEndpointCompany)]
):
    """
    Test
    """

    return ResponsVerifyEndpointCompanyResult(data=credential)
