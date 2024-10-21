from typing import List
from pydantic import Field
from models.shared.modelDataType import BaseModel, ObjectId
from models.shared.modelResponse import ResponseModel

class CompanyFeature(BaseModel):
    name: str
    isActive: bool
    
# ==========================================================

class CompanyConfig(BaseModel):
    features: List[CompanyFeature]

class CompanyConfigView(CompanyConfig):
    id: ObjectId = Field(
        default=...,
        alias="_id",
        title="Id Perusahaan",
        description="Id perusahaan (companyId)"
    )
    """
    companyId
    """

class ResponseCompanyConfigView(ResponseModel):
    data: CompanyConfigView

# ==========================================================

class CompanyConfigFeatureView(BaseModel):
    features: List[CompanyFeature]
    id: ObjectId = Field(
        default=...,
        alias="_id",
        title="Id Perusahaan",
        description="Id perusahaan (companyId)"
    )
    """
    companyId
    """

class ResponseCompanyConfigFeatureView(ResponseModel):
    data: CompanyConfigFeatureView