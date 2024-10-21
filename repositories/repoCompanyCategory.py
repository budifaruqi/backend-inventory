import asyncio
from datetime import datetime
from typing import Any
from classes.classMongoDb import TMongoCollection, TMongoClientSession
from models.company_category.modelCompanyCategory import CompanyCategoryId
from models.company_category.modelCompanyCategoryConsume import CompanyCategoryConsume
from models.shared.modelDataType import ObjectId, TBaseModelObjectId, TGenericBaseModel
from mongodb.mongoCollection import TbCompanyCategory
from mongodb.mongoIndex import index_id, index_company_category


class CompanyCategoryRepository:

    @staticmethod
    async def GetById(
        companyCategoryId: ObjectId,
        *,
        coll: TMongoCollection = TbCompanyCategory,
        session: TMongoClientSession | None = None,
        ignoreDeleted: bool = False,
        resultClass: type[TGenericBaseModel] = CompanyCategoryId
    ) -> TGenericBaseModel | None:
        query: dict[str, Any] = {"_id": companyCategoryId}
        if not ignoreDeleted:
            query["isDeleted"] = False
        dataRaw = await coll.find_one(
            query,
            resultClass.Projection(),
            session=session,
            hint=index_id
        )
        if not dataRaw:
            return None
        else:
            return resultClass(**dataRaw)
    
    @staticmethod
    async def GetByName(
        name: str,
        *,
        coll: TMongoCollection = TbCompanyCategory,
        session: TMongoClientSession | None = None,
        resultClass: type[TGenericBaseModel] = CompanyCategoryId
    ) -> TGenericBaseModel | None:
        dataRaw = await coll.find_one(
            {
                "isDeleted": False,
                "name": name
            },
            resultClass.Projection(),
            session=session,
            hint=index_company_category.isDeleted_name.value.indexName
        )
        if not dataRaw:
            return None
        else:
            return resultClass(**dataRaw)
    
    @staticmethod
    async def Update(
        companyCategoryId: ObjectId,
        param: dict[str, Any],
        *,
        coll: TMongoCollection = TbCompanyCategory,
        session: TMongoClientSession | None = None
    ) -> bool:
        ret = await coll.update_one(
            {
                "_id": companyCategoryId
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
        companyCategoryId: ObjectId,
        param: dict[str, Any],
        updatedBy: ObjectId,
        updatedTime: datetime,
        *,
        coll: TMongoCollection = TbCompanyCategory,
        session: TMongoClientSession | None = None
    ) -> bool:
        param["updatedBy"] = updatedBy
        param["updatedTime"] = updatedTime
        return await CompanyCategoryRepository.Update(
            companyCategoryId,
            param,
            coll=coll,
            session=session
        )
    
    @staticmethod
    async def GetByIds(
        companyCategoryIds: list[ObjectId],
        *,
        coll: TMongoCollection = TbCompanyCategory,
        session: TMongoClientSession | None = None,
        resultClass: type[TGenericBaseModel] = CompanyCategoryId
    ) -> list[TGenericBaseModel]:
        query: dict[str, Any] = {
            "_id": { "$in": companyCategoryIds },
            "isDeleted": False
        }

        cursor = coll.find(
            query,
            resultClass.Projection(),
            session=session,
            hint=index_id
        )
        itemsRaw: list[dict[str, Any]] = await cursor.to_list(None) # type: ignore

        return [resultClass(**item) for item in itemsRaw]
    
    @staticmethod
    async def GetByIdsAsync(
        companyCategoryIds: list[ObjectId],
        *,
        coll: TMongoCollection = TbCompanyCategory,
        session: TMongoClientSession | None = None,
        resultClass: type[TGenericBaseModel] = CompanyCategoryId
    ) -> list[TGenericBaseModel]:
        roleSet = set(companyCategoryIds)
        companyCategoryIds = list(roleSet)
        if len(companyCategoryIds) == 0:
            return []
        
        listRet: list[resultClass] = []
        pageSize = 10
        offset = 0
        lengthRoleIds = len(companyCategoryIds)
        while True:
            lst = await CompanyCategoryRepository.GetByIds(
                companyCategoryIds[offset:offset + pageSize],
                coll=coll,
                session=session,
                resultClass=resultClass
            )
            listRet.extend(lst)
            offset += pageSize
            if offset >= lengthRoleIds:
                break
            # only sleep if page more than 1
            await asyncio.sleep(0)

        return listRet
    
    @staticmethod
    def GetIdFromList(
        companyCategoryId: ObjectId,
        companyCategoryIds: list[TBaseModelObjectId]  
    ) -> TBaseModelObjectId | None:
        for item in companyCategoryIds:
            if item.id == companyCategoryId:
                return item
            
        return None

    @staticmethod
    async def CreateOrUpdate(
        companyCategoryId: ObjectId,
        param: CompanyCategoryConsume,
        *,
        coll: TMongoCollection = TbCompanyCategory,
        session: TMongoClientSession | None = None
    ) -> ObjectId | None:
        d = param.model_dump(by_alias=False, exclude={"id"})
        ret = await coll.update_one(
            {
                "_id": companyCategoryId
            },
            {
                "$set": d
            },
            upsert=True,
            hint=index_id,
            session=session
        )
        if (ret.matched_count > 0):
            return companyCategoryId
        elif ret.upserted_id is not None:
            return ObjectId(ret.upserted_id)
        else:
            return None