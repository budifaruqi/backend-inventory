from pydantic import Field
from models.account.modelAccount import AccountAdditional, AccountDetail, AccountEx, AccountPrivilege
from models.shared.modelAuditData import AuditData
from models.shared.modelDataType import ObjectId


class AccountConsume(
    AuditData,
    AccountPrivilege,
    AccountAdditional,
    AccountEx,
    AccountDetail
):
    id: ObjectId = Field(
        default=...,
        alias="_id"
    )
    """
    accountId
    
    Id Akun
    """