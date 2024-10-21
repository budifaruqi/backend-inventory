from pydantic import Field
from models.company_category.modelCompanyCategory import CompanyCategoryEx
from models.shared.modelAuditData import AuditData
from models.shared.modelDataType import ObjectId


class CompanyCategoryConsume(AuditData, CompanyCategoryEx):
    id: ObjectId = Field(
        default=...,
        alias="_id"
    )
    """
    companyCategoryId
    """