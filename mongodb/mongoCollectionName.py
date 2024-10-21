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
    TbUoMCategory = "uom_category"
    TbUoM= "uom"