from datetime import datetime
from typing import Any, Dict
from classes.classMongoDb import TMongoClientSession, TMongoCollection
from models.account_external.modelAccountExternalCompanyCategory import AccountExternalCompanyCategory
from models.account_external.modelAccountExternalConsume import AccountExternalConsume
from models.shared.modelDataType import ObjectId, TGenericBaseModel
from mongodb.mongoIndex import index_id
from models.account_external.modelAccountExternal import AccountExternalView
from mongodb.mongoCollection import TbAccountExternal


class AccountExternalRepository:

    @staticmethod
    async def GetById(
        accountExternalId: ObjectId,
        *,
        coll: TMongoCollection = TbAccountExternal,
        session: TMongoClientSession | None = None,
        ignoreDeleted: bool = False,
        resultClass: type[TGenericBaseModel] = AccountExternalView,
    ) -> TGenericBaseModel | None:
        query: dict[str, Any] = {"_id": accountExternalId}
        if not ignoreDeleted:
            query["isDeleted"] = False
        dataRaw = await coll.find_one(
            query, resultClass.Projection(), session=session, hint=index_id
        )
        if dataRaw is not None:
            return resultClass(**dataRaw)
        else:
            return None

    @staticmethod
    async def GetByIdAndCompanyCategoryId(
        accountExternalId: ObjectId,
        companyCategoryId: ObjectId,
        *,
        coll: TMongoCollection = TbAccountExternal,
        session: TMongoClientSession | None = None,
        ignoreDeleted: bool = False,
        resultClass: type[TGenericBaseModel] = AccountExternalView
    ) -> TGenericBaseModel | None:
        query: dict[str, Any] = {
            "_id": accountExternalId,
            "companyCategoryIds.companyCategoryId": companyCategoryId
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
    async def Update(
        accountExternalId: ObjectId,
        param: dict[str, Any],
        *,
        coll: TMongoCollection = TbAccountExternal,
        session: TMongoClientSession | None = None,
    ) -> bool:
        ret = await coll.update_one(
            {
                "_id": accountExternalId
            },
            {
                "$set": param
            },
            session=session,
            hint=index_id
        )
        return ret.matched_count == 1

    @staticmethod
    async def UpdateByUser(
        accountExternalId: ObjectId,
        param: dict[str, Any],
        updatedBy: ObjectId,
        updatedTime: datetime,
        *,
        coll: TMongoCollection = TbAccountExternal,
        session: TMongoClientSession | None = None,
    ) -> bool:
        param["updatedBy"] = updatedBy
        param["updatedTime"] = updatedTime
        return await AccountExternalRepository.Update(
            accountExternalId,
            param,
            coll=coll,
            session=session
        )

    @staticmethod
    async def GetCompanyCategory(
        accountExternalId: ObjectId,
        companyCategoryId: ObjectId,
        *,
        coll: TMongoCollection = TbAccountExternal,
        session: TMongoClientSession | None = None,
        resultClass: type[TGenericBaseModel] = AccountExternalCompanyCategory,
    ):
        query: dict[str, Any] = {
            "_id": accountExternalId,
            "isDeleted": False,
            "companyCategoryIds.companyCategoryId": companyCategoryId,
        }
        dataRaw: Dict[str, Any] | None = await coll.find_one(
            query,
            {
                "_id": 0,
                "companyCategoryIds.$": 1
            },
            session=session,
            hint=index_id,
        )
        if dataRaw is not None:
            companyCategoryIds: list[dict[str, Any] | Any] | Any | None = dataRaw.get(
                "companyCategoryIds"
            )
            if (
                (companyCategoryIds is not None)
                and (isinstance(companyCategoryIds, list))
                and (len(companyCategoryIds) > 0)
            ):
                companyCategory = companyCategoryIds[0]
                if isinstance(companyCategory, dict):
                    return resultClass(**companyCategory)
        return None

    @staticmethod
    async def HasCompanyCategory(
        accountExternalId: ObjectId,
        *,
        coll: TMongoCollection = TbAccountExternal,
        session: TMongoClientSession | None = None,
    ) -> bool:
        query: dict[str, Any] = {
            "_id": accountExternalId,
            "isDeleted": False
        }
        dataRaw: Dict[str, Any] | None = await coll.find_one(
            query,
            {
                "_id": -1,
                "companyCategoryIds": {
                    "$slice": 1
                }
            },  # get first element
            session=session,
            hint=index_id,
        )
        if dataRaw is not None:
            # print("HasCompany:", dataRaw)
            companyCategoryIds: list[dict[str, Any] | Any] | Any | None = dataRaw.get(
                "companyCategoryIds"
            )
            if (
                (companyCategoryIds is not None)
                and (isinstance(companyCategoryIds, list))
                and (len(companyCategoryIds) > 0)
            ):
                return len(companyCategoryIds) > 0
        return False

    @staticmethod
    async def CreateOrUpdate(
        accountId: ObjectId,
        param: AccountExternalConsume,
        *,
        coll: TMongoCollection = TbAccountExternal,
        session: TMongoClientSession | None = None
    ) -> ObjectId:
        d = param.model_dump(by_alias=False, exclude={"id"})
        ret = await coll.update_one(
            {
                "_id": accountId
            },
            {
                "$set": d
            },
            upsert=True,
            hint="_id_",
            session=session
        )
        if (ret.matched_count > 0):
            return accountId
        else:
            return ObjectId(ret.upserted_id)
    