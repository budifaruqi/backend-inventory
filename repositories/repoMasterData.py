from datetime import datetime
import re
from typing import Any
from classes.classMongoDb import TMongoClientSession, TMongoCollection
from models.master_data.modelMasterData import MasterDataCreateParam, MasterDataView
from models.shared.modelDataType import BaseModelObjectId, ObjectId, TGenericBaseModel
from mongodb.mongoCollection import TbMasterData
from mongodb.mongoIndex import index_id, index_master_data
from pymongo.results import InsertOneResult


class MasterDataRepository:
    
    @staticmethod
    async def GetById(
        id: ObjectId,
        *,
        coll: TMongoCollection = TbMasterData,
        session: TMongoClientSession | None = None,
        ignoreDeleted: bool = False,
        resultClass: type[TGenericBaseModel] = MasterDataView
    ) :
        query: dict[str, Any] = {"_id": id}
        if not ignoreDeleted:
            query["isDeleted"] = False
        dataRaw = await coll.find_one(
            query,
            resultClass.Projection(),
            session=session,
            hint=index_id
        )
        if dataRaw is not None:
            return resultClass(**dataRaw)
        else:
            return None
    
    @staticmethod
    async def Combo(
        name: str | None ,
        *,
        coll: TMongoCollection = TbMasterData,
        session: TMongoClientSession | None = None,
        resultClass: type[TGenericBaseModel] = MasterDataView
    ):
        query:dict[str, Any]= {
                "isDeleted": False
            }
        if name is not None:
            name = name.strip()
            if len(name) > 0:
                namePattern = re.compile(re.escape(name), re.IGNORECASE)
                query.update(
                    {
                        "name": { "$regex": namePattern}
                    }
                )

        print(query)
        cursor = coll.find(
            query,
            resultClass.Projection(),
            session=session,
            hint=index_master_data.isDeleted_name.value.indexName
        )
        itemsRaw: list[dict[str, Any]] = await cursor.to_list(None) # type: ignore

        return [resultClass(**item) for item in itemsRaw]

    @staticmethod
    async def GetByIdAndCompanyId(
        id: ObjectId,
        companyId: ObjectId,
        *,
        coll: TMongoCollection = TbMasterData,
        session: TMongoClientSession | None = None,
        ignoreDeleted: bool = False,
        resultClass: type[TGenericBaseModel] = MasterDataView
    ):
        query: dict[str, Any] = {
            "_id": id,
            "companyId": companyId
        }
        if not ignoreDeleted:
            query["isDeleted"] = False
        dataRaw = await coll.find_one(
            query,
            resultClass.Projection(),
            session=session,
            hint=index_id
        )
        if dataRaw is not None:
            return resultClass(**dataRaw)
        else:
            return None
    
    @staticmethod
    async def GetByIdAndFollowerCompanyId(
        accountId: ObjectId,
        followerCompanyId: ObjectId,
        *,
        coll: TMongoCollection = TbMasterData,
        session: TMongoClientSession | None = None,
        ignoreDeleted: bool = False,
        resultClass: type[TGenericBaseModel] = MasterDataView
    ):
        query: dict[str, Any] = {
            "_id": accountId,
            "followerCompanyIds": followerCompanyId
        }
        if not ignoreDeleted:
            query["isDeleted"] = False
        dataRaw = await coll.find_one(
            query,
            resultClass.Projection(),
            session=session,
            hint=index_id
        )
        if dataRaw is not None:
            return resultClass(**dataRaw)
        else:
            return None
        
    @staticmethod
    async def NameExists(
        name: str,
        *,
        coll: TMongoCollection = TbMasterData,
        session: TMongoClientSession | None = None,
        resultClass: type[TGenericBaseModel] = BaseModelObjectId
    ):
        query: dict[str, Any] = {
            "isDeleted": False,
            "name": name
        }

        dataRaw = await coll.find_one(
            query,
            resultClass.Projection(),
            session=session,
            hint=index_master_data.isDeleted_name.value.indexName
        )
        if not dataRaw:
            return None
        else:
            return resultClass(**dataRaw)
    
    @staticmethod
    async def Update(
        id: ObjectId,
        param: dict[str, Any],
        *,
        coll: TMongoCollection = TbMasterData,
        session: TMongoClientSession | None = None
    ):
        ret = await coll.update_one(
            {
                "_id": id
            },
            {
                "$set": param
            },
            session=session,
            hint=index_id
        )
        return (ret.matched_count == 1)
    
    @staticmethod
    async def UpdateByUser(
        id: ObjectId,
        param: dict[str, Any],
        updatedBy: ObjectId,
        updatedTime: datetime,
        *,
        coll: TMongoCollection = TbMasterData,
        session: TMongoClientSession | None = None
    ):
        param["updatedBy"] = updatedBy
        param["updatedTime"] = updatedTime
        
        return await MasterDataRepository.Update(
            id,
            param,
            coll=coll,
            session=session
        )
    


    @staticmethod
    async def CreateOrUpdate(
        id:ObjectId,
        param: MasterDataCreateParam,
        *,
        coll: TMongoCollection = TbMasterData,
        session: TMongoClientSession | None = None
    ):
        d = param.model_dump(by_alias=False, exclude={"id"})
        ret = await coll.update_one(
            {
                "_id": id
            },
            {
                "$set": d
            },
            upsert=True,
            hint="_id_",
            session=session
        )
        if (ret.matched_count > 0):
            return id
        else:
            return ObjectId(ret.upserted_id)
        
    @staticmethod
    async def Create(
        request: MasterDataCreateParam,
        *,
        coll: TMongoCollection = TbMasterData,
        session: TMongoClientSession | None = None
    ):
        ret: InsertOneResult = await coll.insert_one(
            request.model_dump(),
            session=session
        )
        if (ret.inserted_id is None):
            return None
        else:
            return ObjectId(ret.inserted_id)

    