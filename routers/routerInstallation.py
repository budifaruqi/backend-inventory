from fastapi import APIRouter
from helpers.helperInstall import InstallHelper

ApiRouter_Install = APIRouter(
    prefix="/install",
    tags=["Installation"]  
)

@ApiRouter_Install.post(
    path="/install",
    response_model=dict,
    operation_id="Install_start",
    summary="Install",
    openapi_extra={
        "x-ignore": True
    }
)
async def ApiRouter_Install_Install(
):
    return await InstallHelper.StartInstall()
