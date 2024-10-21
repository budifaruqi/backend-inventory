from datetime import datetime
from typing import Any
from classes.classMongoDb import TMongoClientSession, TMongoCollection
from models.master_data_follower.enumMasterData import MasterDataFollowerStatus
from models.master_data_follower.modelMasterDataFollower import MasterDataFollowerCreateParam, MasterDataFollowerView
from models.shared.modelDataType import ObjectId, TGenericBaseModel
from mongodb.mongoCollection import TbMasterDataFollower
from mongodb.mongoIndex import index_id, index_master_data_follower
from pymongo.results import InsertOneResult


class MasterDataFollowerRepository:

    @staticmethod
    async def GetById(
        id: ObjectId,
        *,
        coll: TMongoCollection = TbMasterDataFollower,
        session: TMongoClientSession | None = None,
        ignoreDeleted: bool = False,
        resultClass: type[TGenericBaseModel] = MasterDataFollowerView
    ) -> TGenericBaseModel | None:
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
    async def GetByIdAndCompanyId(
        id: ObjectId,
        companyId: ObjectId,
        *,
        coll: TMongoCollection = TbMasterDataFollower,
        session: TMongoClientSession | None = None,
        ignoreDeleted: bool = False,
        resultClass: type[TGenericBaseModel] = MasterDataFollowerView
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
            hint=index_master_data_follower.isDeleted_companyId.value.indexName
        )
        if dataRaw is not None:
            return resultClass(**dataRaw)
        else:
            return None
    
    @staticmethod
    async def GetByMasterDataIdAndCompanyId(
        masterDataId: ObjectId,
        companyId: ObjectId,
        *,
        coll: TMongoCollection = TbMasterDataFollower,
        session: TMongoClientSession | None = None,
        ignoreDeleted: bool = False,
        resultClass: type[TGenericBaseModel] = MasterDataFollowerView
    ):
        query: dict[str, Any] = {
            "masterDataId": masterDataId,
            "companyId": companyId
        }
        if not ignoreDeleted:
            query["isDeleted"] = False
        dataRaw = await coll.find_one(
            query,
            resultClass.Projection(),
            session=session,
            hint=index_master_data_follower.isDeleted_masterDataId_companyId.value.indexName
        )
        if dataRaw is not None:
            return resultClass(**dataRaw)
        else:
            return None
        


    @staticmethod
    async def GetByIdAndStatus(
        id: ObjectId,
        status: MasterDataFollowerStatus,
        *,
        coll: TMongoCollection = TbMasterDataFollower,
        session: TMongoClientSession | None = None,
        ignoreDeleted: bool = False,
        resultClass: type[TGenericBaseModel] = MasterDataFollowerView
    ):
        query: dict[str, Any] = {
            "_id": id,
            "status": status
        }
        if not ignoreDeleted:
            query["isDeleted"] = False
        dataRaw = await coll.find_one(
            query,
            resultClass.Projection(),
            session=session,
            hint=index_master_data_follower.isDeleted_status.value.indexName
        )
        if dataRaw is not None:
            return resultClass(**dataRaw)
        else:
            return None
    
    @staticmethod
    async def Create(
        request: MasterDataFollowerCreateParam,
        *,
        coll: TMongoCollection = TbMasterDataFollower,
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
        
    @staticmethod
    async def Update(
        id: ObjectId,
        param: dict[str, Any],
        *,
        coll: TMongoCollection = TbMasterDataFollower,
        session: TMongoClientSession | None = None
    ) :
        ret = await coll.update_one(
            {
                "_id": id
            },
            {
                "$set": param
            },
            session=session,
            hint="_id_"
        )
        return (ret.matched_count == 1)
    
    @staticmethod
    async def UpdateByUser(
        id: ObjectId,
        param: dict[str, Any],
        updatedBy: ObjectId,
        updatedTime: datetime,
        *,
        coll: TMongoCollection = TbMasterDataFollower,
        session: TMongoClientSession | None = None
    ) -> bool:
        param["updatedBy"] = updatedBy
        param["updatedTime"] = updatedTime
        
        return await MasterDataFollowerRepository.Update(
            id,
            param,
            coll=coll,
            session=session
        )
    
        
