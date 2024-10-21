from datetime import datetime, timezone
import re
from typing import Any
from controller.controllerMasterData import MasterDataController
from models.lead_tags.modelLeadTags import LeadTagCreateCommandRequest, LeadTagCreateWebRequest, LeadTagView
from models.shared.modelDataType import ObjectId
from models.shared.modelEnvironment import MsEnvironment
from models.shared.modelPagination import MsPagination
from mongodb.mongoCollection import TbLeadTag
from mongodb.mongoIndex import index_lead_tag
from repositories.repoLeadTag import LeadTagRepository
from utils.util_http_exception import MsHTTPConflictException, MsHTTPInternalServerErrorException, MsHTTPNotFoundException
from utils.util_http_response import MsHTTPExceptionMessage, MsHTTPExceptionType
from utils.util_pagination import Paginate
from config.config import settings

class MasterLeadTagController:

    @staticmethod
    async def Find(
        masterDataId: ObjectId,
        name: str | None,
        companyId: ObjectId,
        paging: MsPagination
    ):
        
        masterData = await MasterDataController.GetByIdAndCompanyId(
            masterDataId,
            companyId
        )

        query: dict[str, Any] = {
            "isDeleted": False,
            "masterDataId": masterData.id
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
            collection=TbLeadTag,
            query_filter=query,
            params=paging,
            session=None,
            hint=index_lead_tag.isDeleted_masterDataId_name.value.indexName,
            filterItem=True,
            resultItemsClass=LeadTagView,
            explain=True if settings.project.environment == MsEnvironment.development else False
        )

        return data
    
    @staticmethod
    async def GetById(
        id: ObjectId,
    ):
        
        data = await LeadTagRepository.GetById(
            id= id,
            resultClass=LeadTagView
        )

        if data is None:
            raise MsHTTPNotFoundException(MsHTTPExceptionType.NOT_FOUND, MsHTTPExceptionMessage.LEAD_TAG_NOT_FOUND)
        
        return data
    
    @staticmethod
    async def GetByIdAndCompanyId(
        id: ObjectId,
        companyId: ObjectId
    ):
        

        data = await LeadTagRepository.GetByIdAndCompanyId(
            id,
            companyId
        )

        if data is None:
            raise MsHTTPNotFoundException(MsHTTPExceptionType.NOT_FOUND,MsHTTPExceptionMessage.LEAD_TAG_NOT_FOUND)
        
        return data

    @staticmethod
    async def GetByIdAndMasterDataId(
        id: ObjectId,
        companyId: ObjectId,
        masterDataId: ObjectId
    ):
        
        masterData = await MasterDataController.GetByIdAndCompanyId(
            masterDataId,
            companyId
        )

        data = await LeadTagRepository.GetByIdAndMasterDataId(
            id,
            masterData.id
        )

        if data is None:
            raise MsHTTPNotFoundException(MsHTTPExceptionType.NOT_FOUND,MsHTTPExceptionMessage.LEAD_TAG_NOT_FOUND)
        
        return data
    
    @staticmethod
    async def GetByIdAndCompanyIdAndMasterDataId(
        id: ObjectId,
        companyId: ObjectId,
        masterDataId: ObjectId
    ):
        
        masterData = await MasterDataController.GetByIdAndCompanyId(
            masterDataId,
            companyId
        )

        data = await LeadTagRepository.GetByIdAndCompanyIdAndMasterDataId(
            id,
            companyId,
            masterData.id
        )

        if data is None:
            raise MsHTTPNotFoundException(MsHTTPExceptionType.NOT_FOUND,MsHTTPExceptionMessage.LEAD_TAG_NOT_FOUND)
        
        return data
    
    @staticmethod
    async def Create(
        companyId: ObjectId,
        masterDataId: ObjectId,
        request: LeadTagCreateWebRequest,
        createdBy: ObjectId
    ):
        masterData = await MasterDataController.GetByIdAndCompanyId(
            masterDataId,
            companyId
        )

        if await LeadTagRepository.NameExists(
            request.name,
            masterData.id
        ):
            raise MsHTTPConflictException(
                MsHTTPExceptionType.LEAD_TAG_NAME_ALREADY_EXISTS, 
                MsHTTPExceptionMessage.LEAD_TAG_NAME_ALREADY_EXISTS_F.value.format(name=request.name)
                )
        newLeadTagId = await LeadTagRepository.Create(
            LeadTagCreateCommandRequest(
                name=request.name,
                description=request.name,
                masterDataId=masterData.id,
                companyId=companyId,
                createdTime= datetime.now(timezone.utc),
                createdBy=createdBy
            ),
        )
        if not newLeadTagId:
            raise MsHTTPInternalServerErrorException(
                "FAILED_CREATE_LEAD_TAG"
            )
        return newLeadTagId
    
    @staticmethod
    async def UpdateByIdAndCompanyIdAndMasterDataId(
        id: ObjectId,
        companyId: ObjectId,
        masterDataId: ObjectId,
        request: LeadTagCreateWebRequest,
        updatedBy: ObjectId
    ):
        masterData = await MasterDataController.GetByIdAndCompanyId(
            masterDataId,
            companyId
        )

        data = await MasterLeadTagController.GetByIdAndMasterDataId(
            id, companyId, masterData.id
        )

        if data.name != request.name and await LeadTagRepository.NameExists(
            request.name,
            masterData.id
        ):
            raise MsHTTPConflictException(
                MsHTTPExceptionType.LEAD_TAG_NAME_ALREADY_EXISTS, 
                MsHTTPExceptionMessage.LEAD_TAG_NAME_ALREADY_EXISTS_F.value.format(name=request.name)
                )
        
        if not await LeadTagRepository.UpdateByUser(
            data.id,
            {
                "name" : request.name,
                "description": request.description
            },
            updatedBy,
            datetime.now(timezone.utc)
        ):
            raise MsHTTPInternalServerErrorException(
                "FAILED_UPDATE_LEAD_TAG",
                "Gagal mengubah Lead Tag"
            )
        
        updatedData = await MasterLeadTagController.GetByIdAndMasterDataId(data.id, companyId, masterData.id)

        return updatedData
    
    @staticmethod
    async def Delete(
        id: ObjectId,
        companyId: ObjectId,
        masterDataId: ObjectId,
        updatedBy: ObjectId
    ): 
        masterData = await MasterDataController.GetByIdAndCompanyId(
            masterDataId,
            companyId
        )

        leadTag = await MasterLeadTagController.GetByIdAndMasterDataId(
            id,
            companyId,
            masterData.id
        )

        if not await LeadTagRepository.UpdateByUser(
            leadTag.id,
            {
                "isDeleted" : True
            },
            updatedBy,
            datetime.now(timezone.utc)
        ): 
            raise MsHTTPInternalServerErrorException(
                "FAILED_DELETE_LEAD_TAG",
                "Gagal menghapus Lead Tag"
            )
        
        data = await LeadTagRepository.GetByIdAndMasterDataId(
            id,
            masterData.id,
            ignoreDeleted=True
        )
        
        return data
    