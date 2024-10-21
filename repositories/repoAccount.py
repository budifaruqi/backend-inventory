from datetime import datetime
from typing import Any, List, Dict
from classes.classMongoDb import TMongoClientSession, TMongoCollection
from models.account.modelAccountCompany import AccountCompany
from models.account.modelAccountConsume import AccountConsume
from models.shared.modelDataType import BaseModelObjectId, ObjectId, TGenericBaseModel
from mongodb.mongoIndex import index_id, index_account
from models.account.modelAccount import AccountRole, AccountView
from mongodb.mongoCollection import TbAccount


class AccountRepository:

    @staticmethod
    async def GetById(
        accountId: ObjectId,
        *,
        coll: TMongoCollection = TbAccount,
        session: TMongoClientSession | None = None,
        ignoreDeleted: bool = False,
        resultClass: type[TGenericBaseModel] = AccountView
    ) -> TGenericBaseModel | None:
        query: dict[str, Any] = {"_id": accountId}
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
        accountId: ObjectId,
        companyId: ObjectId,
        *,
        coll: TMongoCollection = TbAccount,
        session: TMongoClientSession | None = None,
        ignoreDeleted: bool = False,
        resultClass: type[TGenericBaseModel] = AccountView
    ) -> TGenericBaseModel | None:
        query: dict[str, Any] = {
            "_id": accountId,
            "companyIds.companyId": companyId
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
    async def UsernameExists(
        username: str,
        *,
        coll: TMongoCollection = TbAccount,
        session: TMongoClientSession | None = None,
        resultClass: type[TGenericBaseModel] = BaseModelObjectId
    ) -> TGenericBaseModel | None:
        query: dict[str, Any] = {
            "isDeleted": False,
            "username": username
        }

        dataRaw = await coll.find_one(
            query,
            resultClass.Projection(),
            session=session,
            hint=index_account.isDeleted_username_roles.value.indexName
        )
        if not dataRaw:
            return None
        else:
            return resultClass(**dataRaw)
    
    @staticmethod
    async def EmailExists(
        email: str,
        *,
        coll: TMongoCollection = TbAccount,
        session: TMongoClientSession | None = None,
        resultClass: type[TGenericBaseModel] = BaseModelObjectId
    ) -> TGenericBaseModel | None:
        query: dict[str, Any] = {
            "isDeleted": False,
            "email": email
        }

        dataRaw = await coll.find_one(
            query,
            resultClass.Projection(),
            session=session,
            hint=index_account.isDeleted_email_roles.value.indexName
        )
        if not dataRaw:
            return None
        else:
            return resultClass(**dataRaw)
    
    @staticmethod
    async def PhoneExists(
        phone: str,
        *,
        coll: TMongoCollection = TbAccount,
        session: TMongoClientSession | None = None,
        resultClass: type[TGenericBaseModel] = BaseModelObjectId
    ) -> TGenericBaseModel | None:
        query: dict[str, Any] = {
            "isDeleted": False,
            "phone": phone
        }

        dataRaw = await coll.find_one(
            query,
            resultClass.Projection(),
            session=session,
            hint=index_account.isDeleted_phone_roles.value.indexName
        )
        if not dataRaw:
            return None
        else:
            return resultClass(**dataRaw)
    
    @staticmethod
    async def Update(
        accountId: ObjectId,
        param: dict[str, Any],
        *,
        coll: TMongoCollection = TbAccount,
        session: TMongoClientSession | None = None
    ) -> bool:
        ret = await coll.update_one(
            {
                "_id": accountId
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
        accountId: ObjectId,
        param: dict[str, Any],
        updatedBy: ObjectId,
        updatedTime: datetime,
        *,
        coll: TMongoCollection = TbAccount,
        session: TMongoClientSession | None = None
    ) -> bool:
        param["updatedBy"] = updatedBy
        param["updatedTime"] = updatedTime
        return await AccountRepository.Update(
            accountId,
            param,
            coll=coll,
            session=session
        )
    
    @staticmethod
    async def HasRoleSystem(
        accountId: ObjectId,
        roleId: ObjectId,
        *,
        coll: TMongoCollection = TbAccount,
        session: TMongoClientSession | None = None
    ) -> bool:
        ret = await coll.find_one(
            {
                "_id": accountId,
                "roles": roleId
            },
            {
                "_id": 1
            },
            session=session,
            hint=index_id
        )
        if not ret:
            return False
        else:
            return True
    
    @staticmethod
    async def HasRolesSystem(
        accountId: ObjectId,
        roleIds: List[ObjectId],
        *,
        coll: TMongoCollection = TbAccount,
        session: TMongoClientSession | None = None,
        resultClass: type[TGenericBaseModel] = AccountRole
    ) -> TGenericBaseModel | None:
        ret = await coll.find_one(
            {
                "_id": accountId,
                "roles": { "$in": roleIds }
            },
            {
                "roles.$": 1,
                "_id": 1
            },
            session=session,
            hint=index_id
        )
        if not ret:
            return None
        else:
            return resultClass(**ret)
    
    @staticmethod
    async def RoleSystemCount(
        accountId: ObjectId,
        *,
        coll: TMongoCollection = TbAccount,
        session: TMongoClientSession | None = None
    ) -> int | None:
        cursor = coll.aggregate(
            [
                {
                    "$match": {
                        "_id": accountId
                    }
                },
                {
                    "$project": {
                        "count": {
                            "$size": "$roles"
                        },
                        "_id": 0
                    }
                }
            ],
            session=session,
            hint=index_id
        )
        data: list[dict[str, Any]] = await cursor.to_list(None) # type: ignore
        if len(data) != 1:
            return None
        count = data[0].get("count")
        if isinstance(count, int):
            return count
        else:
            return None
    
    @staticmethod
    async def UserCountByRoleSystem(
        roleId: ObjectId,
        *,
        limit: int | None = None,
        coll: TMongoCollection = TbAccount,
        session: TMongoClientSession | None = None
    ) -> int:
        t = await coll.count_documents(
            {
                "isDeleted": False,
                "roles": roleId
            },
            limit=limit,
            session=session,
            hint=index_account.isDeleted_roles.value.indexName
        )
        return t
    
    @staticmethod
    async def GetCompany(
        accountId: ObjectId,
        companyId: ObjectId,
        *,
        coll: TMongoCollection = TbAccount,
        session: TMongoClientSession | None = None,
        resultClass: type[TGenericBaseModel] = AccountCompany
    ):
        query: dict[str, Any] = {
            "_id": accountId,
            "isDeleted": False,
            "companyIds.companyId": companyId
        }
        dataRaw: Dict[str, Any] | None = await coll.find_one(
            query,
            # {"companyIds.$": 1},
            {
                "_id": 0,
                "companyIds.$": 1
            },
            session=session,
            hint=index_id
        )
        if dataRaw is not None:
            # print("GetCompany:", dataRaw)
            companyIds: list[dict[str, Any] | Any] | Any | None = dataRaw.get("companyIds")
            if (companyIds is not None) and (isinstance(companyIds, list)) and (len(companyIds) > 0):
                company = companyIds[0]
                if isinstance(company, dict):
                    return resultClass(**company)
        return None
    
    @staticmethod
    async def HasCompany(
        accountId: ObjectId,
        *,
        coll: TMongoCollection = TbAccount,
        session: TMongoClientSession | None = None
    ) -> bool:
        query: dict[str, Any] = {
            "_id": accountId,
            "isDeleted": False,
            "companyIds": {
                "$ne": []
            }
        }
        dataRaw = await coll.find_one(
            query,
            {
                "_id": 1
            },
            session=session,
            hint=index_id
        )
        return dataRaw is not None

    @staticmethod
    async def CreateOrUpdate(
        accountId: ObjectId,
        param: AccountConsume,
        *,
        coll: TMongoCollection = TbAccount,
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
    