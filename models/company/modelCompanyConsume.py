from pydantic import Field
from models.company.modelCompany import CompanyDetail, CompanyEx
from models.company.modelCompanyConfig import CompanyConfig
from models.shared.modelAuditData import AuditData
from models.shared.modelDataType import ObjectId


class CompanyConsume(AuditData, CompanyConfig, CompanyEx, CompanyDetail):
    id: ObjectId = Field(
        default=...,
        alias="_id"
    )
    """
    companyId
    """
    
