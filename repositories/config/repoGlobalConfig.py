from datetime import datetime, timezone
from typing import Any
from pymongo.results import InsertOneResult, UpdateResult
from classes.classMongoDb import TMongoClientSession, TMongoCollection
from models.shared.modelDataType import ObjectId
from mongodb.mongoIndex import index_global_config
from models.config.modelGlobalConfig import MsBaseConfig
from mongodb.mongoCollection import TbGlobalConfig

class GlobalConfigRepository:

    @staticmethod
    async def GetById(
        configId: ObjectId,
        *,
        coll: TMongoCollection = TbGlobalConfig,
        session: TMongoClientSession | None = None
    ) -> dict[str, Any] | None:
        configRaw = await coll.find_one(
            {
                "_id": configId
            },
            session=session,
            hint="_id_"
        )
        if not configRaw:
            return None
        else:
            return configRaw
        
    @staticmethod
    async def NameExists(
        name: str,
        *,
        coll: TMongoCollection = TbGlobalConfig,
        session: TMongoClientSession | None = None
    ) -> ObjectId | None:
        config = await coll.find_one(
            {
                "name": name
            },
            {
                "_id": 1
            },
            session=session,
            hint=index_global_config.index_name.value.indexName
        )
        if not config:
            return None
        else:
            return ObjectId(config.get("_id"))
        
    @staticmethod
    async def GetByName(
        name: str,
        *,
        coll: TMongoCollection = TbGlobalConfig,
        session: TMongoClientSession | None = None
    ) -> dict[str, Any] | None:
        config = await coll.find_one(
            {
                "name": name
            },
            session=session,
            hint=index_global_config.index_name.value.indexName
        )
        if not config:
            return None
        else:
            return config
        
    @staticmethod
    async def GetDataByName(
        name: str,
        *,
        coll: TMongoCollection = TbGlobalConfig,
        session: TMongoClientSession | None = None
    ) -> dict[str, Any] | None:
        config = await coll.find_one(
            {
                "name": name
            },
            {
                "_id": -1,
                "data": 1
            },
            session=session,
            hint=index_global_config.index_name.value.indexName
        )
        if not config:
            return None
        else:
            return config
        
    @staticmethod
    async def Create(
        param: MsBaseConfig,
        *,
        coll: TMongoCollection = TbGlobalConfig,
        session: TMongoClientSession | None = None
    ) -> ObjectId | None:
        ret: InsertOneResult = await coll.insert_one(
            param.model_dump(),
            session=session
        )
        if (ret.inserted_id is None):
            return None
        else:
            return ObjectId(ret.inserted_id)
        
    @staticmethod
    async def Update(
        configId: ObjectId,
        param: MsBaseConfig,
        *,
        coll: TMongoCollection = TbGlobalConfig,
        session: TMongoClientSession | None = None
    ) -> bool:
        param.updatedTime = datetime.now(timezone.utc)
        ret: UpdateResult = await coll.update_one(
            {
                "_id": configId
            },
            {
                "$set": param.model_dump()
            },
            session=session,
            hint="_id_"
        )
        return (ret.matched_count == 1)
        
    @staticmethod
    async def UpdateByName(
        name: str,
        param: MsBaseConfig,
        *,
        coll: TMongoCollection = TbGlobalConfig,
        session: TMongoClientSession | None = None,
        upsert: bool = False
    ) -> bool:
        param.updatedTime = datetime.now(timezone.utc)
        ret: UpdateResult = await coll.update_one(
            {
                "name": name
            },
            {
                "$set": param.model_dump()
            },
            upsert=upsert,
            session=session,
            hint=index_global_config.index_name.value.indexName
        )
        return (ret.matched_count == 1)
