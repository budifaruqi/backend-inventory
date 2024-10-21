from datetime import datetime, timezone
from typing import Any
from pymongo.read_concern import ReadConcern
from pymongo.read_preferences import ReadPreference
from pymongo.write_concern import WriteConcern
from classes.classMongoDb import TMongoClientSession
from controller.controllerMasterData import MasterDataController
from models.master_data_follower.enumMasterData import MasterDataFollowerStatus
from models.master_data_follower.modelMasterDataFollower import MasterDataFollowerApproveRequest, MasterDataFollowerCreateParam, MasterDataFollowerView
from models.shared.modelDataType import ObjectId
from models.shared.modelEnvironment import MsEnvironment
from models.shared.modelPagination import MsPagination
from models.uom.modelUoMCategory import UoMCategoryView
from mongodb.mongoClient import MongoDbStartDefaultSession
from mongodb.mongoCollection import TbMasterDataFollower
from mongodb.mongoIndex import index_master_data_follower, index_uom_category
from repositories.repoMasterDataFollower import MasterDataFollowerRepository
from utils.util_http_exception import MsHTTPConflictException, MsHTTPInternalServerErrorException, MsHTTPNotFoundException
from utils.util_http_response import MsHTTPExceptionMessage, MsHTTPExceptionType
from utils.util_pagination import Paginate
from config.config import settings


class MasterDataFollowerController:

    @staticmethod
    async def Find(
        masterDataId: ObjectId | None,
        status: MasterDataFollowerStatus | None,
        companyId: ObjectId | None,
        paging: MsPagination
    ):

        query: dict[str, Any] = {
                "isDeleted": False,
                "masterDataId": masterDataId
            }
        query.update({
            "companyId": companyId if companyId is not None else None,
            "status": status if status is not None else None,
        })

        # Remove None values from the query
        query = {k: v for k, v in query.items() if v is not None}
        print(query)

        # Paginate and return results
        data = await Paginate(
            collection=TbMasterDataFollower,
            query_filter=query,
            params=paging,
            session=None,
            hint=index_uom_category.isDeleted_companyId_name.value.indexName,
            filterItem=True,
            resultItemsClass=UoMCategoryView,
            explain=True if settings.project.environment == MsEnvironment.development else False
        )

        return data
    
    @staticmethod
    async def GetById(
        id:ObjectId,
        *,
        session: TMongoClientSession | None = None
    ):
        data = await UoMCategoryRepository.GetById(
            id,
            session=session
        )

        if data is None:
            raise MsHTTPNotFoundException(MsHTTPExceptionType.NOT_FOUND,MsHTTPExceptionMessage.MASTER_DATA_FOLLOWER_NOT_FOUND)
        
        return data

    @staticmethod
    async def GetByIdAndCompanyId(
        id:ObjectId,
        companyId:ObjectId,
        *,
        session: TMongoClientSession | None = None
    ):
        data = await MasterDataFollowerRepository.GetByIdAndCompanyId(
            id = id,
            companyId = companyId,
            session=session,
            resultClass=MasterDataFollowerView
        )

        if data is None:
            raise MsHTTPNotFoundException(MsHTTPExceptionType.NOT_FOUND, MsHTTPExceptionMessage.MASTER_DATA_FOLLOWER_NOT_FOUND)
        
        return data
    
    @staticmethod
    async def GetByIdAndStatus(
        id:ObjectId,
        status: MasterDataFollowerStatus,
        *,
        session: TMongoClientSession | None = None
    ):
        data = await MasterDataFollowerRepository.GetByIdAndStatus(
            id,
            status,
            session=session
        )

        if data is None:
            raise MsHTTPNotFoundException(MsHTTPExceptionType.NOT_FOUND, MsHTTPExceptionMessage.STATUS_NOT_MATCH)
        
        return data
    
    @staticmethod
    async def Create(
        companyId: ObjectId,
        masterDataId: ObjectId,
        createdBy: ObjectId
    ):
        masterData = await MasterDataController.GetById(masterDataId)

        if await MasterDataFollowerRepository.GetByMasterDataIdAndCompanyId(
            masterDataId,
            companyId
        ):
            raise MsHTTPConflictException(
                MsHTTPExceptionType.ALREADY_EXISTS,
                MsHTTPExceptionMessage.MASTER_DATA_FOLLOWER_ALREADY_EXIST)

        newMasterDataFollowerId = await MasterDataFollowerRepository.Create(
            MasterDataFollowerCreateParam(
                companyId=companyId,
                masterDataId=masterData.id,
                status=MasterDataFollowerStatus.REQUESTED,
                createdTime= datetime.now(timezone.utc),
                createdBy=createdBy
            ),
        )
        if not newMasterDataFollowerId:
            raise MsHTTPInternalServerErrorException(
                type="FAILED_CREATE_MASTER_DATA_Follower"
            )
        return newMasterDataFollowerId
    
    @staticmethod
    async def UpdateStatusById(
        companyId : ObjectId,
        id: ObjectId,
        status: MasterDataFollowerStatus,
        updatedBy: ObjectId
    ): 
        async def _coro(
            session: TMongoClientSession,
            _companyId: ObjectId,
            _id: ObjectId,
            _status: MasterDataFollowerStatus,
            _updatedBy: ObjectId
        ): 

            masterDataFollower = await MasterDataFollowerController.GetById(
                _id,
                session=session
            )

            await MasterDataFollowerController.GetByIdAndStatus(
                _id,
                MasterDataFollowerStatus.REQUESTED,
                session=session
            )

            masterData = await MasterDataController.GetByIdAndCompanyId(
                masterDataFollower.masterDataId,
                _companyId,
                session = session
            )

            if not await MasterDataFollowerRepository.Update(
                id=masterDataFollower.id,
                param={
                    "status": _status,
                    "updatedBy": _updatedBy,
                    "updatedTime":datetime.now(timezone.utc).replace(tzinfo=None)
                },
                session=session
            ):
                raise MsHTTPInternalServerErrorException(
                    type="UPDATE_MASTER_DATA_FOLLOWER_STATUS_FAILED",
                    message="Gagal menyetujui request Master Data"
                )
            
            followerCompanyIds = masterData.followerCompanyIds

            if masterDataFollower.id not in followerCompanyIds:
                followerCompanyIds.append(masterDataFollower.id)  # Add new ID


            await MasterDataController.UpdateFollower(
                masterData.id,
                followerCompanyIds,
                companyId,
                datetime.now(timezone.utc).replace(tzinfo=None),
                updatedBy,
                session=session
            )

            updatedData = await MasterDataFollowerController.GetById(
                _id,
                session=session
            )
            return updatedData
        
        async with await MongoDbStartDefaultSession() as session:
            ret: MasterDataFollowerView = await session.with_transaction(
                lambda s: _coro(s, companyId, id,status, updatedBy),  # type: ignore
                read_concern=ReadConcern("snapshot"),
                write_concern=WriteConcern(w="majority", wtimeout=1000),
                read_preference=ReadPreference.PRIMARY
            )
            return ret
        
    @staticmethod
    async def UpdateConfigById(
        companyId : ObjectId,
        id: ObjectId,
        config: MasterDataFollowerApproveRequest,
        updatedBy: ObjectId
    ): 
        
        masterDataFollower = await MasterDataFollowerController.GetById(
            id
        )

        await MasterDataFollowerController.GetByIdAndStatus(
            id,
            MasterDataFollowerStatus.APPROVE
        )

        await MasterDataController.GetByIdAndCompanyId(
            masterDataFollower.masterDataId,
            companyId
        )

        # Get existing config
        existing_config = masterDataFollower.config

        # Update only the specific config from the request
        for incoming_setting in config.config:
            for existing_setting in existing_config:
                if incoming_setting.data == existing_setting.data:
                    # Replace operations with what is provided in the request
                    existing_setting.operations = incoming_setting.operations

        config_dict = [setting.model_dump() for setting in existing_config]

        if not await MasterDataFollowerRepository.Update(
            id=masterDataFollower.id,
            param={
                "config": config_dict,
                "updatedBy": updatedBy,
                "updatedTime":datetime.now(timezone.utc).replace(tzinfo=None)
            }
        ):
            raise MsHTTPInternalServerErrorException(
                type="UPDATE_CONFIG_MASTER_DATA_FOLLOWER_FAILED",
                message="Gagal update config Master Data Follower"
            )

        updatedData: MasterDataFollowerView = await MasterDataFollowerController.GetById(
            id
        )
        return updatedData
        
    
        