import asyncio
from datetime import datetime
import re
from typing import Any
from classes.classMongoDb import TMongoCollection, TMongoClientSession
from models.company.modelCompanyConsume import CompanyConsume
from models.shared.modelDataType import ObjectId, TGenericBaseModel
from models.company.modelCompany import CompanyView
from models.company.modelCompanyConfig import CompanyConfigView
from mongodb.mongoCollection import TbCompany
from mongodb.mongoIndex import index_id, index_company


class CompanyRepository:

    @staticmethod
    async def GetById(
        companyId: ObjectId,
        *,
        coll: TMongoCollection = TbCompany,
        session: TMongoClientSession | None = None,
        ignoreDeleted: bool = False,
        resultClass: type[TGenericBaseModel] = CompanyView
    ) -> TGenericBaseModel | None:
        query: dict[str, Any] = {"_id": companyId}
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
    async def GetByInitial(
        initial: str,
        *,
        coll: TMongoCollection = TbCompany,
        session: TMongoClientSession | None = None,
        resultClass: type[TGenericBaseModel] = CompanyView
    ) -> TGenericBaseModel | None:
        dataRaw = await coll.find_one(
            {
                "isDeleted": False,
                "initial": initial
            },
            resultClass.Projection(),
            session=session,
            hint=index_company.isDeleted_initial.value.indexName
        )
        if not dataRaw:
            return None
        else:
            return resultClass(**dataRaw)

    @staticmethod
    async def GetConfig(
        companyId: ObjectId,
        *,
        coll: TMongoCollection = TbCompany,
        session: TMongoClientSession | None = None,
        resultClass: type[TGenericBaseModel] = CompanyConfigView
    ) -> TGenericBaseModel | None:
        query: dict[str, Any] = {
            "_id": companyId,
            "isDeleted": False
        }
        dataRaw = await coll.find_one(
            query,
            CompanyConfigView.Projection(),
            session=session,
            hint=index_id
        )
        if not dataRaw:
            return None
        else:
            return resultClass(**dataRaw)
    
    @staticmethod
    async def InitialExists(
        initial: str,
        *,
        coll: TMongoCollection = TbCompany,
        session: TMongoClientSession | None = None
    ) -> ObjectId | None:
        dataRaw = await coll.find_one(
            {
                "isDeleted": False,
                "initial": initial
            },
            {"_id": 1},
            session=session,
            hint=index_company.isDeleted_initial.value.indexName
        )
        if not dataRaw:
            return None
        else:
            return ObjectId(dataRaw.get("_id"))
    
    @staticmethod
    async def NameExists(
        name: str,
        *,
        coll: TMongoCollection = TbCompany,
        session: TMongoClientSession | None = None
    ) -> ObjectId | None:
        namePattern = re.compile("^" + re.escape(name) + "$", re.IGNORECASE)
        dataRaw = await coll.find_one(
            {
                "isDeleted": False,
                "name": { "$regex": namePattern }
            },
            {"_id": 1},
            session=session,
            hint=index_company.isDeleted_name.value.indexName
        )
        if not dataRaw:
            return None
        else:
            return ObjectId(dataRaw.get("_id"))
    
    @staticmethod
    async def Update(
        companyId: ObjectId,
        param: dict[str, Any],
        *,
        coll: TMongoCollection = TbCompany,
        session: TMongoClientSession | None = None
    ) -> bool:
        ret = await coll.update_one(
            {
                "_id": companyId
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
        companyId: ObjectId,
        param: dict[str, Any],
        updatedBy: ObjectId,
        updatedTime: datetime,
        *,
        coll: TMongoCollection = TbCompany,
        session: TMongoClientSession | None = None
    ) -> bool:
        param["updatedBy"] = updatedBy
        param["updatedTime"] = updatedTime
        return await CompanyRepository.Update(
            companyId,
            param,
            coll=coll,
            session=session
        )
    
    @staticmethod
    async def GetByIds(
        companyIds: list[ObjectId],
        *,
        coll: TMongoCollection = TbCompany,
        session: TMongoClientSession | None = None,
        resultClass: type[TGenericBaseModel] = CompanyView
    ) -> list[TGenericBaseModel]:
        query: dict[str, Any] = {
            "_id": { "$in": companyIds },
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
        companyIds: list[ObjectId],
        *,
        coll: TMongoCollection = TbCompany,
        session: TMongoClientSession | None = None,
        resultClass: type[TGenericBaseModel] = CompanyView,
        pageSize: int = 10
    ) -> list[TGenericBaseModel]:
        roleSet = set(companyIds)
        companyIds = list(roleSet)
        if len(companyIds) == 0:
            return []
        
        listRet: list[resultClass] = []
        if pageSize < 1:
            pageSize = 10
        offset = 0
        lengthRoleIds = len(companyIds)
        while True:
            lst = await CompanyRepository.GetByIds(
                companyIds=companyIds[offset:offset + pageSize],
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
    async def CreateOrUpdate(
        companyId: ObjectId,
        param: CompanyConsume,
        *,
        coll: TMongoCollection = TbCompany,
        session: TMongoClientSession | None = None
    ) -> ObjectId | None:
        d = param.model_dump(by_alias=False, exclude={"id"})
        ret = await coll.update_one(
            {
                "_id": companyId
            },
            {
                "$set": d
            },
            upsert=True,
            hint=index_id,
            session=session
        )
        if (ret.matched_count > 0):
            return companyId
        elif ret.upserted_id is not None:
            return ObjectId(ret.upserted_id)
        else:
            return None
    

    