from pydantic import Field
from models.account_external.modelAccountExternal import AccountExternalDetail, AccountExternalEx, AccountExternalIdentity, AccountExternalPrivilege
from models.shared.modelAuditData import AuditData
from models.shared.modelDataType import ObjectId


class AccountExternalConsume(
    AuditData,
    AccountExternalPrivilege,
    AccountExternalEx,
    AccountExternalIdentity,
    AccountExternalDetail
):
    id: ObjectId = Field(
        default=...,
        alias="_id"
    )
    """
    accountExternalId
    
    Id Akun Eksternal
    """
