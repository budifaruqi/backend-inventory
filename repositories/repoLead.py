from datetime import datetime
import re
from typing import Any
from models.lead.enumLead import LeadStatus, LeadType
from models.lead.modelLead import LeadCreateCommandRequest, LeadView
from models.shared.modelDataType import ObjectId
from classes.classMongoDb import TMongoClientSession, TMongoCollection
from models.shared.modelDataType import BaseModelObjectId, ObjectId, TGenericBaseModel
from mongodb.mongoCollection import TbLead
from mongodb.mongoIndex import index_id, index_lead
from pymongo.results import InsertOneResult

class LeadRepository:

    @staticmethod
    async def GetById(
        id: ObjectId,
        *,
        coll: TMongoCollection = TbLead,
        session: TMongoClientSession | None = None,
        ignoreDeleted: bool = False,
        resultClass: type[TGenericBaseModel] = LeadView
    ) -> TGenericBaseModel | None:
        query: dict[str, Any] = {"_id": id}
        if not ignoreDeleted:
            query["isDeleted"] = False
        dataRaw: dict[str, Any] | None = await coll.find_one(
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
        coll: TMongoCollection = TbLead,
        session: TMongoClientSession | None = None,
        ignoreDeleted: bool = False,
        resultClass: type[TGenericBaseModel] = LeadView
    ) -> TGenericBaseModel | None:
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
            hint=index_lead.isDeleted_companyId.value.indexName
        )
        if dataRaw is not None:
            return resultClass(**dataRaw)
        else:
            return None
    
    @staticmethod
    async def GetByIdAndMasterDataId(
        id: ObjectId,
        masterDataId: ObjectId,
        *,
        coll: TMongoCollection = TbLead,
        session: TMongoClientSession | None = None,
        ignoreDeleted: bool = False,
        resultClass: type[TGenericBaseModel] = LeadView
    ) :
        query: dict[str, Any] = {
            "_id": id,
            "masterDataId": masterDataId
        }
        if not ignoreDeleted:
            query["isDeleted"] = False
        dataRaw = await coll.find_one(
            query,
            resultClass.Projection(),
            session=session,
            hint=index_lead.isDeleted_masterDataId.value.indexName
        )
        if dataRaw is not None:
            return resultClass(**dataRaw)
        else:
            return None
    
    @staticmethod
    async def GetByIdAndCompanyIdAndMasterDataId(
        id: ObjectId,
        companyId: ObjectId,
        masterDataId: ObjectId,
        *,
        coll: TMongoCollection = TbLead,
        session: TMongoClientSession | None = None,
        ignoreDeleted: bool = False,
        resultClass: type[TGenericBaseModel] = LeadView
    ) :
        query: dict[str, Any] = {
            "_id": id,
            "companyId": companyId,
            "masterDataId": masterDataId
        }
        if not ignoreDeleted:
            query["isDeleted"] = False
        dataRaw = await coll.find_one(
            query,
            resultClass.Projection(),
            session=session,
            hint=index_lead.isDeleted_masterDataId_companyId.value.indexName
        )
        if dataRaw is not None:
            return resultClass(**dataRaw)
        else:
            return None
        
    @staticmethod
    async def Combo(
        masterDataId: ObjectId,
        name: str | None,
        type: LeadType | None,
        partnerId: ObjectId | None,
        status: LeadStatus | None,
        tags: list[str] | None,
        *,
        coll: TMongoCollection = TbLead,
        session: TMongoClientSession | None = None,
        resultClass: type[TGenericBaseModel] = LeadView
    ):
        query: dict[str, Any]= {
            "isDeleted": False,
            "masterDataId": masterDataId
        }
        query.update({
            "name": {"$regex": re.compile(re.escape(name.strip()), re.IGNORECASE)} 
            if name and name.strip() else None,
            "type": type if type is not None else None,
            "partnerId": partnerId if partnerId is not None else None,
            "status": status if status is not None else None,
            "tags": {"$all": tags} if tags else None
        })

        # Remove None values from the query
        query = {k: v for k, v in query.items() if v is not None}

        print(query)
        cursor = coll.find(
            query,
            resultClass.Projection(),
            session=session,
            hint=index_lead.isDeleted_masterDataId_name_type_partnerId_status_tags.value.indexName
        )
        itemsRaw: list[dict[str, Any]] = await cursor.to_list(None)  # type: ignore

        return [resultClass(**item) for item in itemsRaw]
        
    # @staticmethod
    # async def GetByIdAndCompanyIdAndMasterDataIdAndType(
    #     id: ObjectId,
    #     companyId: ObjectId,
    #     masterDataId: ObjectId,
    #     type: LeadType,
    #     *,
    #     coll: TMongoCollection = TbLead,
    #     session: TMongoClientSession | None = None,
    #     ignoreDeleted: bool = False,
    #     resultClass: type[TGenericBaseModel] = LeadView
    # ) :
    #     query: dict[str, Any] = {
    #         "_id": id,
    #         "companyId": companyId,
    #         "masterDataId": masterDataId,
    #         "type": type
    #     }
    #     if not ignoreDeleted:
    #         query["isDeleted"] = False
    #     dataRaw = await coll.find_one(
    #         query,
    #         resultClass.Projection(),
    #         session=session,
    #         hint=index_lead.isDeleted_masterDataId_companyId_type.value.indexName
    #     )
    #     if dataRaw is not None:
    #         return resultClass(**dataRaw)
    #     else:
    #         return None

    @staticmethod
    async def NameExists(
        name: str,
        masterDataId: ObjectId,
        *,
        coll: TMongoCollection = TbLead,
        session: TMongoClientSession | None = None,
        resultClass: type[TGenericBaseModel] = BaseModelObjectId
    ) :
        query: dict[str, Any] = {
            "isDeleted": False,
            "masterDataId": masterDataId,
            "name": name
        }

        dataRaw = await coll.find_one(
            query,
            resultClass.Projection(),
            session=session,
            hint=index_lead.isDeleted_masterDataId_name.value.indexName
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
        coll: TMongoCollection = TbLead,
        session: TMongoClientSession | None = None
    ) -> bool:
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
        coll: TMongoCollection = TbLead,
        session: TMongoClientSession | None = None
    ) :
        param["updatedBy"] = updatedBy
        param["updatedTime"] = updatedTime
        return await LeadRepository.Update(
            id,
            param,
            coll=coll,
            session=session
        )
    
    @staticmethod
    async def Create(
        request: LeadCreateCommandRequest,
        *,
        coll: TMongoCollection = TbLead,
        session: TMongoClientSession | None = None
    )  :
        ret: InsertOneResult = await coll.insert_one(
            request.model_dump(),
            session=session
        )
        if (ret.inserted_id is None):
            return None
        else:
            return ObjectId(ret.inserted_id)