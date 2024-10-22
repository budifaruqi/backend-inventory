from datetime import datetime
import re
from typing import Any
from classes.classMongoDb import TMongoClientSession, TMongoCollection
from models.shared.modelDataType import BaseModelObjectId, ObjectId, TGenericBaseModel
from models.uom.modelUoM import UoMCreateCommandRequest, UoMView
from mongodb.mongoCollection import TbUom
from mongodb.mongoIndex import index_id, index_uom
from pymongo.results import InsertOneResult

class UoMRepository:

    @staticmethod
    async def GetById(
    id: ObjectId,
    *,
    coll: TMongoCollection = TbUom,
    session: TMongoClientSession | None = None,
    ignoreDeleted: bool = False,
    resultClass: type[TGenericBaseModel] = UoMView
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
        name: str | None,
        categoryId: ObjectId | None,
        isActive: bool | None,
        companyId: ObjectId,
        *,
        coll: TMongoCollection = TbUom,
        session: TMongoClientSession | None = None,
        resultClass: type[TGenericBaseModel] = UoMView
    ):
        query:dict[str, Any]= {
                "isDeleted": False,
                "companyId": companyId
            }
        query.update({
            "name": {"$regex": re.compile(re.escape(name.strip()), re.IGNORECASE)} 
            if name and name.strip() else None,
            "categoryId": categoryId if categoryId is not None else None,
            "isActive": isActive if isActive is not None else None
        })

        # Remove None values from the query
        query = {k: v for k, v in query.items() if v is not None}
        print(query)

        cursor = coll.find(
            query,
            resultClass.Projection(),
            session=session,
            hint=index_uom.isDeleted_companyId_isActive_categoryId_name.value.indexName
        )
        itemsRaw: list[dict[str, Any]] = await cursor.to_list(None) # type: ignore

        return [resultClass(**item) for item in itemsRaw]

    @staticmethod
    async def GetByIdAndCompanyId(
        id: ObjectId,
        companyId: ObjectId,
        *,
        coll: TMongoCollection = TbUom,
        session: TMongoClientSession | None = None,
        ignoreDeleted: bool = False,
        resultClass: type[TGenericBaseModel] = UoMView
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
    async def NameExists(
        name: str,
        companyId: ObjectId,
        *,
        coll: TMongoCollection = TbUom,
        session: TMongoClientSession | None = None,
        resultClass: type[TGenericBaseModel] = BaseModelObjectId
    ):
        query: dict[str, Any] = {
            "isDeleted": False,
            "companyId": companyId,
            "name": name
        }

        dataRaw = await coll.find_one(
            query,
            resultClass.Projection(),
            session=session,
            hint=index_uom.isDeleted_companyId_name.value.indexName
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
        coll: TMongoCollection = TbUom,
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
        coll: TMongoCollection = TbUom,
        session: TMongoClientSession | None = None
    ):
        param["updatedBy"] = updatedBy
        param["updatedTime"] = updatedTime
        
        return await UoMRepository.Update(
            id,
            param,
            coll=coll,
            session=session
        )
    


    @staticmethod
    async def CreateOrUpdate(
        id:ObjectId,
        param: UoMCreateCommandRequest,
        *,
        coll: TMongoCollection = TbUom,
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
        request: UoMCreateCommandRequest,
        *,
        coll: TMongoCollection = TbUom,
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
