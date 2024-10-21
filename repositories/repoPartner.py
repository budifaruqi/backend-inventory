from datetime import datetime
from typing import Any
from classes.classMongoDb import TMongoClientSession, TMongoCollection
from models.partner.enumPartnerType import PartnerType
from models.partner.modelPartner import PartnerCreateCommandRequest, PartnerView
from models.shared.modelDataType import BaseModelObjectId, ObjectId, TGenericBaseModel
from mongodb.mongoCollection import TbPartner
from mongodb.mongoIndex import index_id, index_partner
from pymongo.results import InsertOneResult

class PartnerRepository:

    @staticmethod
    async def Exists(
        id: ObjectId,
        *,
        coll: TMongoCollection = TbPartner,
        session: TMongoClientSession | None = None,
        ignoreDeleted: bool = False
    ) :
        query: dict[str, Any] = {"_id": id}
        if not ignoreDeleted:
            query["isDeleted"] = False

        exists = await coll.find_one(
            query,
            {"_id": 1},  # We only need the `_id` field to check for existence
            session=session,
            hint=index_id
        )

        return exists is not None

    @staticmethod
    async def GetById(
        id: ObjectId,
        *,
        coll: TMongoCollection = TbPartner,
        session: TMongoClientSession | None = None,
        ignoreDeleted: bool = False,
        resultClass: type[TGenericBaseModel] = PartnerView
    ):
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
        coll: TMongoCollection = TbPartner,
        session: TMongoClientSession | None = None,
        ignoreDeleted: bool = False,
        resultClass: type[TGenericBaseModel] = PartnerView
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
            hint=index_partner.isDeleted_companyId.value.indexName
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
        coll: TMongoCollection = TbPartner,
        session: TMongoClientSession | None = None,
        ignoreDeleted: bool = False,
        resultClass: type[TGenericBaseModel] = PartnerView
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
            hint=index_partner.isDeleted_masterDataId.value.indexName
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
        coll: TMongoCollection = TbPartner,
        session: TMongoClientSession | None = None,
        ignoreDeleted: bool = False,
        resultClass: type[TGenericBaseModel] = PartnerView
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
            hint=index_partner.isDeleted_masterDataId_companyId.value.indexName
        )
        if dataRaw is not None:
            return resultClass(**dataRaw)
        else:
            return None
        
    @staticmethod
    async def GetByIdAndCompanyIdAndMasterDataIdAndType(
        id: ObjectId,
        companyId: ObjectId,
        masterDataId: ObjectId,
        type: PartnerType,
        *,
        coll: TMongoCollection = TbPartner,
        session: TMongoClientSession | None = None,
        ignoreDeleted: bool = False,
        resultClass: type[TGenericBaseModel] = PartnerView
    ) :
        query: dict[str, Any] = {
            "_id": id,
            "companyId": companyId,
            "masterDataId": masterDataId,
            "type": type
        }
        if not ignoreDeleted:
            query["isDeleted"] = False
        dataRaw = await coll.find_one(
            query,
            resultClass.Projection(),
            session=session,
            hint=index_partner.isDeleted_masterDataId_companyId_type.value.indexName
        )
        if dataRaw is not None:
            return resultClass(**dataRaw)
        else:
            return None

    @staticmethod
    async def NameExists(
        name: str,
        masterDataId: ObjectId,
        *,
        coll: TMongoCollection = TbPartner,
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
            hint=index_partner.isDeleted_masterDataId_name.value.indexName
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
        coll: TMongoCollection = TbPartner,
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
        coll: TMongoCollection = TbPartner,
        session: TMongoClientSession | None = None
    ) :
        param["updatedBy"] = updatedBy
        param["updatedTime"] = updatedTime
        return await PartnerRepository.Update(
            id,
            param,
            coll=coll,
            session=session
        )
    
    @staticmethod
    async def Create(
        request: PartnerCreateCommandRequest,
        *,
        coll: TMongoCollection = TbPartner,
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