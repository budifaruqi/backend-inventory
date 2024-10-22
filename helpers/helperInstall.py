from datetime import datetime, timezone
from typing import Any, List
from fastapi.encoders import jsonable_encoder
from bson import SON
from classes.classMongoDb import TMongoCollection
from mongodb.mongoIndex import MongoIndex, index_account, index_account_external, index_company, index_company_category, index_global_config, index_lead, index_lead_tag, index_master_data, index_master_data_follower, index_partner, index_uom_category
from utils.util_logger import msLogger
from mongodb.mongoClient import MGDB
from mongodb.mongoCollection import TbAccount, TbAccountExternal, TbCompany, TbCompanyCategory, TbGlobalConfig, TbLeadTag, TbMasterData, TbMasterDataFollower, TbPartner, TbLead, TbUomCategory, TbUom
from mongodb.mongoCollectionName import CollectionNames

class MongoIndexInit:
    def __init__(self, coll: TMongoCollection, collName: str, indexs: list[MongoIndex]) -> None:
        self.coll = coll
        self.collName = collName
        self.indexs = indexs

ListMongoIndexInit: list[MongoIndexInit] = [
    MongoIndexInit(TbGlobalConfig, CollectionNames.TbGlobalConfig.value, indexs=[i.value for i in index_global_config]),
    MongoIndexInit(TbCompanyCategory, CollectionNames.TbCompanyCategory.value, indexs=[i.value for i in index_company_category]),
    MongoIndexInit(TbCompany, CollectionNames.TbCompany.value, indexs=[i.value for i in index_company]),
    MongoIndexInit(TbAccount, CollectionNames.TbAccount.value, indexs=[i.value for i in index_account]),
    MongoIndexInit(TbAccountExternal, CollectionNames.TbAccountExternal.value, indexs=[i.value for i in index_account_external]),
    MongoIndexInit(TbPartner, CollectionNames.TbPartner.value, indexs=[i.value for i in index_partner]),
    MongoIndexInit(TbMasterData, CollectionNames.TbMasterData.value, indexs=[i.value for i in index_master_data]),
    MongoIndexInit(TbMasterDataFollower, CollectionNames.TbMasterDataFollower.value, indexs=[i.value for i in index_master_data_follower]),
    MongoIndexInit(TbLead, CollectionNames.TbLead.value, indexs=[i.value for i in index_lead]),
    MongoIndexInit(TbLeadTag, CollectionNames.TbLeadTag.value, indexs=[i.value for i in index_lead_tag]),
    MongoIndexInit(TbUomCategory, CollectionNames.TbUomCategory.value, indexs=[i.value for i in index_uom_category]),


]

class InstallHelper:

    @staticmethod
    async def StartInstall(
    ) -> dict[str, Any]:
        log: dict[str, Any] = {}
        listCollection = await MGDB.list_collection_names()
        startTime = datetime.now(timezone.utc)
        try:
            log = await InstallHelper._CreateIndexs(listCollection, log, startTime)

        except Exception as err:
            msLogger.exception(str(err), err)
            log["error"] = str(err)
        return jsonable_encoder(log)

    @staticmethod
    def CollectionHasIndex(indexes: List[SON[str, Any] | Any], indexName: str) -> bool:
        for ind in indexes:
            if not isinstance(ind, SON):
                continue
            if not ind.has_key("name"): # type: ignore
                continue
            indName = ind.get("name") # type: ignore
            if indName == indexName:
                return True
        return False

    @staticmethod
    async def _DoCreateIndex(m: MongoIndexInit, listCollection: List[str], log: dict[str, Any], startTime: datetime) -> dict[str, Any]:
        subLog: dict[str, Any] = {}
        if not m.collName in listCollection:
            await MGDB.create_collection(m.collName)
            subLog[m.collName + "_collection"] = "created"
        else:
            subLog[m.collName + "_collection"] = "already exists"

        indexesCur = m.coll.list_indexes()
        indexes: List[Any] = await indexesCur.to_list(None) # type: ignore
        for idx in m.indexs:
            indexName = idx.indexName
            if not InstallHelper.CollectionHasIndex(indexes, indexName):
                await m.coll.create_index(
                    [(i.field, i.sort) for i in idx.keys],
                    name=indexName,
                    **idx.kwargs
                )
                subLog[m.collName + "_" + indexName] = "created"
            else:
                subLog[m.collName + "_" + indexName] = "already exists"

        return subLog

    @staticmethod
    async def _CreateIndexs(listCollection: List[str], log: dict[str, Any], startTime: datetime) -> dict[str, Any]:
        for indexInit in ListMongoIndexInit:
            retIndex = await InstallHelper._DoCreateIndex(indexInit, listCollection, log, startTime)
            log["setup_" + indexInit.collName] = retIndex
        return log

