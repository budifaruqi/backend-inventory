from enum import Enum


class CollectionNames(str, Enum):
    TbGlobalConfig = "global_config"
    TbCompanyCategory = "company_category"
    TbCompany = "company"
    TbAccount = "account"
    TbAccountExternal = "account_external"
    TbPartner = "partner"
    TbMasterData="master_data"
    TbMasterDataFollower="master_data_follower"
    TbLeadTag="lead_tag"
    TbLead="lead"
    TbUomCategory = "uom_category"
    TbUom= "uom"
    TbGenericMaterialCategory="generic_material_category"
    TbGenericMaterial="generic_material"