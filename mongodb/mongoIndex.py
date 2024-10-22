from enum import Enum
from typing import Any, Mapping

import pymongo

class MongoIndexKey:
    def __init__(self, field: str, sort: int | str | Mapping[str, Any]) -> None:
        self.field = field
        self.sort = sort

class MongoIndex:
    def __init__(self, indexName: str, keys: list[MongoIndexKey], **kwargs: Any) -> None:
        self.indexName = indexName
        self.keys = keys
        self.kwargs = kwargs

# ---------------------------------------------------------------------------------------------------------
index_id = "_id_"
# ---------------------------------------------------------------------------------------------------------
class index_global_config(Enum):
    index_name = MongoIndex(
        "index_name",
        [
            MongoIndexKey("name", pymongo.ASCENDING)
        ]
    )
# ---------------------------------------------------------------------------------------------------------
class index_company_category(Enum):
    isDeleted_name = MongoIndex(
        "index_isDeleted_name",
        [
            MongoIndexKey("isDeleted", pymongo.ASCENDING),
            MongoIndexKey("name", pymongo.ASCENDING)
        ]
    )
# ---------------------------------------------------------------------------------------------------------
class index_company(Enum):
    isDeleted_initial = MongoIndex(
        "index_isDeleted_initial",
        [
            MongoIndexKey("isDeleted", pymongo.ASCENDING),
            MongoIndexKey("initial", pymongo.ASCENDING)
        ]
    )
    isDeleted_name = MongoIndex(
        "index_isDeleted_name",
        [
            MongoIndexKey("isDeleted", pymongo.ASCENDING),
            MongoIndexKey("name", pymongo.ASCENDING)
        ]
    )
    isDeleted_companyCategoryId = MongoIndex(
        "index_isDeleted_companyCategoryId",
        [
            MongoIndexKey("isDeleted", pymongo.ASCENDING),
            MongoIndexKey("companyCategoryId", pymongo.ASCENDING)
        ]
    )
# ---------------------------------------------------------------------------------------------------------
class index_account(Enum):
    isDeleted_name_roles = MongoIndex(
        "index_isDeleted_name_roles",
        [
            MongoIndexKey("isDeleted", pymongo.ASCENDING),
            MongoIndexKey("name", pymongo.ASCENDING),
            MongoIndexKey("roles", pymongo.ASCENDING)
        ]
    )
    isDeleted_username_roles = MongoIndex(
        "index_isDeleted_username_roles",
        [
            MongoIndexKey("isDeleted", pymongo.ASCENDING),
            MongoIndexKey("username", pymongo.ASCENDING),
            MongoIndexKey("roles", pymongo.ASCENDING)
        ]
    )
    isDeleted_email_roles = MongoIndex(
        "index_isDeleted_email_roles",
        [
            MongoIndexKey("isDeleted", pymongo.ASCENDING),
            MongoIndexKey("email", pymongo.ASCENDING),
            MongoIndexKey("roles", pymongo.ASCENDING)
        ]
    )
    isDeleted_phone_roles = MongoIndex(
        "index_isDeleted_phone_roles",
        [
            MongoIndexKey("isDeleted", pymongo.ASCENDING),
            MongoIndexKey("phone", pymongo.ASCENDING),
            MongoIndexKey("roles", pymongo.ASCENDING)
        ]
    )
    isDeleted_roles = MongoIndex(
        "index_isDeleted_roles",
        [
            MongoIndexKey("isDeleted", pymongo.ASCENDING),
            MongoIndexKey("roles", pymongo.ASCENDING)
        ]
    )
    isDeleted_companyIds_companyId = MongoIndex(
        "index_isDeleted_companyIds.companyId",
        [
            MongoIndexKey("isDeleted", pymongo.ASCENDING),
            MongoIndexKey("companyIds.companyId", pymongo.ASCENDING)
        ]
    )
# ---------------------------------------------------------------------------------------------------------
class index_account_external(Enum):
    isDeleted_name = MongoIndex(
        "index_isDeleted_name",
        [
            MongoIndexKey("isDeleted", pymongo.ASCENDING),
            MongoIndexKey("name", pymongo.ASCENDING)
        ]
    )
    isDeleted_username = MongoIndex(
        "index_isDeleted_usernames",
        [
            MongoIndexKey("isDeleted", pymongo.ASCENDING),
            MongoIndexKey("username", pymongo.ASCENDING)
        ]
    )
    isDeleted_email = MongoIndex(
        "index_isDeleted_email",
        [
            MongoIndexKey("isDeleted", pymongo.ASCENDING),
            MongoIndexKey("email", pymongo.ASCENDING)
        ]
    )
    isDeleted_phone = MongoIndex(
        "index_isDeleted_phone",
        [
            MongoIndexKey("isDeleted", pymongo.ASCENDING),
            MongoIndexKey("phone", pymongo.ASCENDING)
        ]
    )
    isDeleted_companyCategoryIds_companyCategoryId = MongoIndex(
        "index_isDeleted_companyCategoryIds.companyCategoryId",
        [
            MongoIndexKey("isDeleted", pymongo.ASCENDING),
            MongoIndexKey("companyCategoryIds.companyCategoryId", pymongo.ASCENDING)
        ]
    )

# ---------------------------------------------------------------------------------------------------------

class index_master_data(Enum):
    isDeleted_name = MongoIndex(
        "index_isDeleted_name",
        [
            MongoIndexKey("isDeleted", pymongo.ASCENDING),
            MongoIndexKey("name", pymongo.ASCENDING)
        ]
    )
# ---------------------------------------------------------------------------------------------------------

class index_uom_category(Enum):
    isDeleted_name = MongoIndex(
        "index_isDeleted_name",
        [
            MongoIndexKey("isDeleted", pymongo.ASCENDING),
            MongoIndexKey("name", pymongo.ASCENDING)
        ]
    )
    isDeleted_companyId_name = MongoIndex(
        "index_isDeleted_companyId_name",
        [
            MongoIndexKey("isDeleted", pymongo.ASCENDING),
            MongoIndexKey("companyId", pymongo.ASCENDING),
            MongoIndexKey("name", pymongo.ASCENDING)
        ]
    )
# ---------------------------------------------------------------------------------------------------------

class index_uom(Enum):
    isDeleted_name = MongoIndex(
        "index_isDeleted_name",
        [
            MongoIndexKey("isDeleted", pymongo.ASCENDING),
            MongoIndexKey("name", pymongo.ASCENDING)
        ]
    )
    isDeleted_companyId_name = MongoIndex(
        "index_isDeleted_companyId_name",
        [
            MongoIndexKey("isDeleted", pymongo.ASCENDING),
            MongoIndexKey("companyId", pymongo.ASCENDING),
            MongoIndexKey("name", pymongo.ASCENDING)
        ]
    )
    isDeleted_companyId_categoryId = MongoIndex(
        "index_isDeleted_companyId_categoryId",
        [
            MongoIndexKey("isDeleted", pymongo.ASCENDING),
            MongoIndexKey("companyId", pymongo.ASCENDING),
            MongoIndexKey("categoryId", pymongo.ASCENDING)
        ]
    )
    isDeleted_companyId_isActive_categoryId_name = MongoIndex(
        "index_isDeleted_companyId_isActive_categoryId_name",
        [
            MongoIndexKey("isDeleted", pymongo.ASCENDING),
            MongoIndexKey("companyId", pymongo.ASCENDING),
            MongoIndexKey("isActive", pymongo.ASCENDING),
            MongoIndexKey("categoryId", pymongo.ASCENDING),
            MongoIndexKey("name", pymongo.ASCENDING)
        ]
    )
# ---------------------------------------------------------------------------------------------------------
class index_generic_material_category(Enum):
    isDeleted_name = MongoIndex(
        "index_isDeleted_name",
        [
            MongoIndexKey("isDeleted", pymongo.ASCENDING),
            MongoIndexKey("name", pymongo.ASCENDING)
        ]
    )
    isDeleted_companyId_name = MongoIndex(
        "index_isDeleted_companyId_name",
        [
            MongoIndexKey("isDeleted", pymongo.ASCENDING),
            MongoIndexKey("companyId", pymongo.ASCENDING),
            MongoIndexKey("name", pymongo.ASCENDING)
        ]
    )
# ---------------------------------------------------------------------------------------------------------
class index_generic_material(Enum):
    isDeleted_name = MongoIndex(
        "index_isDeleted_name",
        [
            MongoIndexKey("isDeleted", pymongo.ASCENDING),
            MongoIndexKey("name", pymongo.ASCENDING)
        ]
    )
    isDeleted_companyId_name = MongoIndex(
        "index_isDeleted_companyId_name",
        [
            MongoIndexKey("isDeleted", pymongo.ASCENDING),
            MongoIndexKey("companyId", pymongo.ASCENDING),
            MongoIndexKey("name", pymongo.ASCENDING)
        ]
    )
    isDeleted_companyId_name_categoryId = MongoIndex(
        "index_isDeleted_companyId_name_categoryId",
        [
            MongoIndexKey("isDeleted", pymongo.ASCENDING),
            MongoIndexKey("companyId", pymongo.ASCENDING),
            MongoIndexKey("name", pymongo.ASCENDING),
            MongoIndexKey("categoryId", pymongo.ASCENDING)
        ]
    )
# ---------------------------------------------------------------------------------------------------------

class index_master_data_follower(Enum):
    isDeleted_name = MongoIndex(
        "index_isDeleted_name",
        [
            MongoIndexKey("isDeleted", pymongo.ASCENDING),
            MongoIndexKey("name", pymongo.ASCENDING)
        ]
    )
    isDeleted_masterDataId_companyId  = MongoIndex(
        "index_isDeleted_masterDataId_companyId",
        [
            MongoIndexKey("isDeleted", pymongo.ASCENDING),
            MongoIndexKey("masterDataId", pymongo.ASCENDING),
            MongoIndexKey("companyId", pymongo.ASCENDING)
        ]
    )
    isDeleted_companyId = MongoIndex(
        "index_isDeleted_companyId",
        [
            MongoIndexKey("isDeleted", pymongo.ASCENDING),
            MongoIndexKey("companyId", pymongo.ASCENDING)
        ]
    )
    isDeleted_companyId_name = MongoIndex(
        "index_isDeleted_companyId_name",
        [
            MongoIndexKey("isDeleted", pymongo.ASCENDING),
            MongoIndexKey("companyId", pymongo.ASCENDING),
            MongoIndexKey("name", pymongo.ASCENDING)
        ]
    )
    isDeleted_status = MongoIndex(
        "index_isDeleted_status",
        [
            MongoIndexKey("isDeleted", pymongo.ASCENDING),
            MongoIndexKey("status", pymongo.ASCENDING)
        ]
    )
# ---------------------------------------------------------------------------------------------------------

class index_lead(Enum):
    isDeleted_masterDataId = MongoIndex(
        "index_isDeleted_masterDataId",
        [
            MongoIndexKey("isDeleted", pymongo.ASCENDING),
            MongoIndexKey("masterDataId", pymongo.ASCENDING)
        ]
    )
    isDeleted_companyId = MongoIndex(
        "index_isDeleted_companyId",
        [
            MongoIndexKey("isDeleted", pymongo.ASCENDING),
            MongoIndexKey("companyId", pymongo.ASCENDING)
        ]
    )
    isDeleted_name = MongoIndex(
        "index_isDeleted_name",
        [
            MongoIndexKey("isDeleted", pymongo.ASCENDING),
            MongoIndexKey("name", pymongo.ASCENDING)
        ]
    )
    isDeleted_masterDataId_companyId = MongoIndex(
        "index_isDeleted_masterDataId_companyId",
        [
            MongoIndexKey("isDeleted", pymongo.ASCENDING),
            MongoIndexKey("masterDataId", pymongo.ASCENDING),
            MongoIndexKey("companyId", pymongo.ASCENDING)
        ]
    )
    isDeleted_masterDataId_name = MongoIndex(
        "index_isDeleted_masterDataId_name",
        [
            MongoIndexKey("isDeleted", pymongo.ASCENDING),
            MongoIndexKey("masterDataId", pymongo.ASCENDING),
            MongoIndexKey("name", pymongo.ASCENDING)
        ]
    )
    isDeleted_masterDataId_companyId_name = MongoIndex(
        "index_isDeleted_masterDataId_companyId_name",
        [
            MongoIndexKey("isDeleted", pymongo.ASCENDING),
            MongoIndexKey("masterDataId", pymongo.ASCENDING),
            MongoIndexKey("companyId", pymongo.ASCENDING),
            MongoIndexKey("name", pymongo.ASCENDING)
        ]
    )
    isDeleted_masterDataId_name_type_partnerId_status_tags = MongoIndex(
        "index_isDeleted_masterDataId_name_type_partnerId_status_tags",
        [
            MongoIndexKey("isDeleted", pymongo.ASCENDING),
            MongoIndexKey("masterDataId", pymongo.ASCENDING),
            MongoIndexKey("name", pymongo.ASCENDING),
            MongoIndexKey("type", pymongo.ASCENDING),
            MongoIndexKey("partnerId", pymongo.ASCENDING),
            MongoIndexKey("status", pymongo.ASCENDING),
            MongoIndexKey("tags", pymongo.ASCENDING)
        ]
    )

# ---------------------------------------------------------------------------------------------------------

class index_lead_tag(Enum):
    isDeleted_masterDataId = MongoIndex(
        "index_isDeleted_masterDataId",
        [
            MongoIndexKey("isDeleted", pymongo.ASCENDING),
            MongoIndexKey("masterDataId", pymongo.ASCENDING)
        ]
    )
    isDeleted_companyId = MongoIndex(
        "index_isDeleted_companyId",
        [
            MongoIndexKey("isDeleted", pymongo.ASCENDING),
            MongoIndexKey("companyId", pymongo.ASCENDING)
        ]
    )
    isDeleted_name = MongoIndex(
        "index_isDeleted_name",
        [
            MongoIndexKey("isDeleted", pymongo.ASCENDING),
            MongoIndexKey("name", pymongo.ASCENDING)
        ]
    )
    isDeleted_masterDataId_companyId = MongoIndex(
        "index_isDeleted_masterDataId_companyId",
        [
            MongoIndexKey("isDeleted", pymongo.ASCENDING),
            MongoIndexKey("masterDataId", pymongo.ASCENDING),
            MongoIndexKey("companyId", pymongo.ASCENDING)
        ]
    )
    isDeleted_masterDataId_name = MongoIndex(
        "index_isDeleted_masterDataId_name",
        [
            MongoIndexKey("isDeleted", pymongo.ASCENDING),
            MongoIndexKey("masterDataId", pymongo.ASCENDING),
            MongoIndexKey("name", pymongo.ASCENDING)
        ]
    )
    isDeleted_masterDataId_companyId_name = MongoIndex(
        "index_isDeleted_masterDataId_companyId_name",
        [
            MongoIndexKey("isDeleted", pymongo.ASCENDING),
            MongoIndexKey("masterDataId", pymongo.ASCENDING),
            MongoIndexKey("companyId", pymongo.ASCENDING),
            MongoIndexKey("name", pymongo.ASCENDING)
        ]
    )

# ---------------------------------------------------------------------------------------------------------
class index_partner(Enum):
    isDeleted_masterDataId = MongoIndex(
        "index_isDeleted_masterDataId",
        [
            MongoIndexKey("isDeleted", pymongo.ASCENDING),
            MongoIndexKey("masterDataId", pymongo.ASCENDING)
        ]
    )
    isDeleted_companyId = MongoIndex(
        "index_isDeleted_companyId",
        [
            MongoIndexKey("isDeleted", pymongo.ASCENDING),
            MongoIndexKey("companyId", pymongo.ASCENDING)
        ]
    )
    isDeleted_masterDataId_name = MongoIndex(
        "index_isDeleted_masterDataId_name",
        [
            MongoIndexKey("isDeleted", pymongo.ASCENDING),
            MongoIndexKey("masterDataId", pymongo.ASCENDING),
            MongoIndexKey("name", pymongo.ASCENDING)
        ]
    )
    isDeleted_masterDataId_companyId = MongoIndex(
        "index_isDeleted_masterDataId_companyId",
        [
            MongoIndexKey("isDeleted", pymongo.ASCENDING),
            MongoIndexKey("masterDataId", pymongo.ASCENDING),
            MongoIndexKey("companyId", pymongo.ASCENDING)
        ]
    )
    isDeleted_masterDataId_companyId_type = MongoIndex(
        "index_isDeleted_masterDataId_companyId_type",
        [
            MongoIndexKey("isDeleted", pymongo.ASCENDING),
            MongoIndexKey("masterDataId", pymongo.ASCENDING),
            MongoIndexKey("companyId", pymongo.ASCENDING),
            MongoIndexKey("type", pymongo.ASCENDING)
        ]
    )
    isDeleted_masterDataId_companyId_name = MongoIndex(
        "index_isDeleted_masterDataId_companyId_name",
        [
            MongoIndexKey("isDeleted", pymongo.ASCENDING),
            MongoIndexKey("masterDataId", pymongo.ASCENDING),
            MongoIndexKey("companyId", pymongo.ASCENDING),
            MongoIndexKey("name", pymongo.ASCENDING)
        ]
    )
    isDeleted_masterDataId_name_type_parentId = MongoIndex(
        "index_isDeleted_masterDataId_name_type_parentId",
        [
            MongoIndexKey("isDeleted", pymongo.ASCENDING),
            MongoIndexKey("masterDataId", pymongo.ASCENDING),
            MongoIndexKey("name", pymongo.ASCENDING),
            MongoIndexKey("type", pymongo.ASCENDING),
            MongoIndexKey("parentId", pymongo.ASCENDING)
        ]
    )
    isDeleted_name_type_parentId = MongoIndex(
        "index_isDeleted_name_type_parentId",
        [
            MongoIndexKey("isDeleted", pymongo.ASCENDING),
            MongoIndexKey("name", pymongo.ASCENDING),
            MongoIndexKey("type", pymongo.ASCENDING),
            MongoIndexKey("parentId", pymongo.ASCENDING)
        ]
    )