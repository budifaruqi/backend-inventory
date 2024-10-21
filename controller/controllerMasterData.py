
from datetime import datetime
import re
from typing import Any
from classes.classMongoDb import TMongoClientSession
from models.master_data.modelMasterData import MasterDataCreateParam, MasterDataCreateRequest, MasterDataView
from models.shared.modelDataType import ObjectId
from models.shared.modelEnvironment import MsEnvironment
from models.shared.modelPagination import MsPagination, MsPaginationResult
from mongodb.mongoCollection import TbMasterData
from mongodb.mongoIndex import index_master_data
from repositories.repoMasterData import MasterDataRepository
from utils.util_http_exception import MsHTTPConflictException, MsHTTPInternalServerErrorException, MsHTTPNotFoundException
from utils.util_http_response import MsHTTPExceptionMessage, MsHTTPExceptionType
from utils.util_pagination import Paginate
from config.config import settings

class MasterDataController:

    @staticmethod
    async def Find(
        name: str | None ,
        companyId: ObjectId,
        paging: MsPagination
    ) -> MsPaginationResult[MasterDataView]:
        query: dict[str, Any] = {
                "isDeleted": False,
                "companyId": companyId
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

        # Paginate and return results
        data = await Paginate(
            collection=TbMasterData,
            query_filter=query,
            params=paging,
            session=None,
            hint=index_master_data.isDeleted_name.value.indexName,
            filterItem=True,
            resultItemsClass=MasterDataView,
            explain=True if settings.project.environment == MsEnvironment.development else False
        )

        return data
        
    @staticmethod
    async def Combo(
        name: str | None
    ):
        data = await MasterDataRepository.Combo(
            name
        )

        return data
        
    @staticmethod
    async def GetById(
        id: ObjectId,
    ):
        
        data = await MasterDataRepository.GetById(
            id
        )

        if data is None:
            raise MsHTTPNotFoundException(MsHTTPExceptionType.NOT_FOUND, MsHTTPExceptionMessage.MASTER_DATA_NOT_FOUND)
        
        return data
    
    @staticmethod
    async def GetByIdAndCompanyId(
        id: ObjectId,
        companyId: ObjectId,
        *,
        session: TMongoClientSession | None = None
    ):
        
        data = await MasterDataRepository.GetByIdAndCompanyId(
            id= id,
            companyId=companyId,
            session=session,
            resultClass=MasterDataView
        )

        if data is None:
            raise MsHTTPNotFoundException(MsHTTPExceptionType.NOT_FOUND,MsHTTPExceptionMessage.MASTER_DATA_NOT_FOUND)
        
        return data
    
    @staticmethod
    async def Create(
        request: MasterDataCreateRequest,
        companyId: ObjectId,
        createdTime: datetime,
        createdBy: ObjectId
    ):
        if await MasterDataRepository.NameExists(
            request.name
        ):
            raise MsHTTPConflictException(
                MsHTTPExceptionType.MASTER_DATA_NAME_ALREADY_EXISTS, 
                MsHTTPExceptionMessage.MASTER_DATA_NAME_ALREADY_EXISTS_F.value.format(name=request.name)
                )
        newMasterDataId = await MasterDataRepository.Create(
            MasterDataCreateParam(
                name=request.name,
                companyId=companyId,
                createdTime= createdTime,
                createdBy=createdBy 
            ),
        )
        if not newMasterDataId:
            raise MsHTTPInternalServerErrorException(
                type="FAILED_CREATE_MASTER_DATA"
            )
        return newMasterDataId
    
    @staticmethod
    async def UpdateByIdAndCompanyId(
        id: ObjectId,
        request: MasterDataCreateRequest,
        companyId: ObjectId,
        updatedTime: datetime,
        updatedBy: ObjectId
    ): 
        data = await MasterDataController.GetByIdAndCompanyId(
            id, companyId
        )
        if data.name == request.name: 
            return data

        if await MasterDataRepository.NameExists(
            request.name
        ):
            raise MsHTTPConflictException(
                MsHTTPExceptionType.MASTER_DATA_NAME_ALREADY_EXISTS, 
                MsHTTPExceptionMessage.MASTER_DATA_NAME_ALREADY_EXISTS_F.value.format(name=request.name)
                )

        if not await MasterDataRepository.UpdateByUser(
            data.id,
            {
                "name" : request.name
            },
            updatedBy,
            updatedTime
        ): 
            raise MsHTTPInternalServerErrorException(
                "FAILED_UPDATE_MASTER_DATA",
                "Gagal mengubah Master Data"
            )
        
        updatedData = await MasterDataController.GetByIdAndCompanyId(data.id, companyId)

        return updatedData
    
    @staticmethod
    async def UpdateFollower(
        id: ObjectId,
        followerCompanyIds: list[ObjectId],
        companyId: ObjectId,
        updatedTime: datetime,
        updatedBy: ObjectId,
        *,
        session: TMongoClientSession | None = None
    ):
        data = await MasterDataController.GetByIdAndCompanyId(
            id, companyId, session=session
        )
        await MasterDataRepository.UpdateByUser(
            id,
            {
                "followerCompanyIds" : followerCompanyIds
            },
            updatedBy,
            updatedTime,
            session=session 
        )
        
        updatedData = await MasterDataRepository.GetByIdAndCompanyId(data.id, companyId, session=session)

        return updatedData
        

    @staticmethod
    async def Delete(
        id: ObjectId,
        companyId: ObjectId,
        updatedTime: datetime,
        updatedBy: ObjectId
    ): 
        data = await MasterDataController.GetByIdAndCompanyId(
            id,
            companyId
        )

        if not await MasterDataRepository.UpdateByUser(
            data.id,
            {
                "isDeleted" : True
            },
            updatedBy,
            updatedTime
        ): 
            raise MsHTTPInternalServerErrorException(
                "FAILED_DELETE_MASTER_DATA",
                "Gagal menghapus Master Data"
            )
        
        deletedData = await MasterDataRepository.GetByIdAndCompanyId(
            id,
            companyId,
            ignoreDeleted=True
        )
        
        return deletedData