from datetime import datetime, timezone
import re
from typing import Any
from classes.classMongoDb import TMongoClientSession
from controller.controllerMasterData import MasterDataController
from models.lead.enumLead import LeadStatus, LeadType
from models.lead.modelLead import LeadCreateCommandRequest, LeadCreateWebRequest, LeadView
from models.shared.modelDataType import ObjectId
from models.shared.modelEnvironment import MsEnvironment
from models.shared.modelPagination import MsPagination
from mongodb.mongoCollection import TbLead
from mongodb.mongoIndex import index_lead
from repositories.repoLead import LeadRepository
from repositories.repoLeadTag import LeadTagRepository
from repositories.repoPartner import PartnerRepository
from utils.util_http_exception import MsHTTPBadRequestException, MsHTTPConflictException, MsHTTPInternalServerErrorException, MsHTTPNotFoundException
from utils.util_http_response import MsHTTPExceptionMessage, MsHTTPExceptionType
from utils.util_pagination import Paginate
from config.config import settings

class MasterLeadController:

    @staticmethod
    async def Find(
        masterDataId: ObjectId,
        name: str | None,
        type: LeadType | None,
        partnerId: ObjectId | None,
        status: LeadStatus | None,
        tags: list[str] | None,
        companyId: ObjectId,
        paging: MsPagination
    ):
        masterData = await MasterDataController.GetByIdAndCompanyId(
            masterDataId,
            companyId
        )
        query: dict[str, Any]= {
            "isDeleted": False,
            "masterDataId": masterData.id
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

        # Paginate and return results
        data = await Paginate(
            collection=TbLead,
            query_filter=query,
            params=paging,
            session=None,
            hint=index_lead.isDeleted_masterDataId_name_type_partnerId_status_tags.value.indexName,
            filterItem=True,
            resultItemsClass=LeadView,
            explain=True if settings.project.environment == MsEnvironment.development else False
        )

        return data
    
    @staticmethod
    async def Combo(
        masterDataId: ObjectId,
        name: str | None,
        type: LeadType | None,
        partnerId: ObjectId | None,
        status: LeadStatus | None,
        tags: list[str] | None,
        companyId: ObjectId
    ):
        masterData = await MasterDataController.GetByIdAndCompanyId(
            masterDataId,
            companyId
        )

        data = await LeadRepository.Combo(
            masterData.id,
            name,
            type,
            partnerId,
            status,
            tags
        )
        return data
    
    @staticmethod
    async def GetById(
        id: ObjectId,
        companyId: ObjectId
    ):
        data= await LeadRepository.GetByIdAndCompanyId(
            id=id,
            companyId=companyId
        )
        if data is None:
            raise MsHTTPNotFoundException(MsHTTPExceptionType.NOT_FOUND)
        
        return data
    
    @staticmethod
    async def GetByIdAndMasterDataId(
        id: ObjectId,
        companyId: ObjectId,
        masterDataId: ObjectId,
        *,
        session: TMongoClientSession | None = None
    ):
        
        masterData = await MasterDataController.GetByIdAndCompanyId(
            masterDataId,
            companyId,
            session=session
        )
        data = await LeadRepository.GetByIdAndMasterDataId(
            id,
            masterData.id,
            session=session
        )
        if data is None:
            raise MsHTTPNotFoundException(MsHTTPExceptionType.NOT_FOUND,MsHTTPExceptionMessage.PARTNER_NOT_FOUND)
        
        return data
    
    @staticmethod
    async def Create(
        companyId: ObjectId,
        masterDataId: ObjectId,
        request: LeadCreateWebRequest,
        createdBy: ObjectId
    ):
        masterData = await MasterDataController.GetByIdAndCompanyId(
            masterDataId,
            companyId
        )
        
        if await LeadRepository.NameExists(
            request.name,
            masterData.id
        ):
            raise MsHTTPConflictException(
                MsHTTPExceptionType.LEAD_NAME_ALREADY_EXISTS, 
                MsHTTPExceptionMessage.LEAD_NAME_ALREADY_EXISTS_F.value.format(name=request.name)
                )
        
        if request.leadTags:
            for tagId in request.leadTags:
                if not await LeadTagRepository.Exists(tagId):
                    raise MsHTTPBadRequestException(
                        "INVALID_LEAD_TAG_ID",
                        "Lead Tag ID: {tagId} tidak ditemukan"
                    )
        if request.partnerId:
            if not await PartnerRepository.Exists(request.partnerId):
                raise MsHTTPBadRequestException(
                        "INVALID_PARTNER_ID",
                        "Partner ID: {request.partnerId} tidak ditemukan"
                    )
        
        #check sales id 

        newLeadId = await LeadRepository.Create(
            LeadCreateCommandRequest(
                name=request.name,
                email=request.email,
                phone=request.phone,
                requirementList=request.requirementList,
                pic=request.pic,
                potentialRevenue=request.potentialRevenue,
                potentialSize=request.potentialSize,
                leadTags=request.leadTags,
                partnerId=request.partnerId,
                salesId=request.salesId,
                companyId=companyId,
                masterDataId=masterData.id,
                type= LeadType.POTENTIAL_LEAD,
                status=LeadStatus.NEW,
                createdTime=datetime.now(timezone.utc),
                createdBy=createdBy
            )
        )
        if not newLeadId:
            raise MsHTTPInternalServerErrorException("FAILED_CREATE_LEAD")
        
        newLead = await MasterLeadController.GetByIdAndMasterDataId(newLeadId, companyId, masterData.id)

        return newLead
    
    @staticmethod
    async def Update(
        id: ObjectId,
        companyId: ObjectId,
        masterDataId: ObjectId,
        request: LeadCreateWebRequest,
        updatedBy: ObjectId
    ):
        masterData = await MasterDataController.GetByIdAndCompanyId(
            masterDataId,
            companyId
        )

        lead = await MasterLeadController.GetByIdAndMasterDataId(
            id,
            companyId,
            masterData.id
        )
        
        if lead.name != request.name and await LeadRepository.NameExists(
            request.name,
            masterData.id
        ):
            raise MsHTTPConflictException(
                MsHTTPExceptionType.LEAD_NAME_ALREADY_EXISTS, 
                MsHTTPExceptionMessage.LEAD_NAME_ALREADY_EXISTS_F.value.format(name=request.name)
                )
        
        if request.leadTags:
            for tagId in request.leadTags:
                if not await LeadTagRepository.Exists(tagId):
                    raise MsHTTPBadRequestException(
                        "INVALID_LEAD_TAG_ID",
                        "Lead Tag ID: {tagId} tidak ditemukan"
                    )
        if request.partnerId:
            if not await PartnerRepository.Exists(request.partnerId):
                raise MsHTTPBadRequestException(
                        "INVALID_PARTNER_ID",
                        "Partner ID: {request.partnerId} tidak ditemukan"
                    )
        
        #check sales id 

        if not await LeadRepository.UpdateByUser(
            lead.id,
            {
                "name": request.name,
                "email": request.email,
                "phone": request.phone,
                "requirementList": request.requirementList,
                "pic": request.pic,
                "potentialRevenue": request.potentialRevenue,
                "potentialSize": request.potentialSize,
                "leadTags": request.leadTags,
                "partnerId": request.partnerId,
                "salesId": request.salesId
            },
            updatedBy,
            datetime.now(timezone.utc)
        ):
            raise MsHTTPInternalServerErrorException("FAILED_UPDATE_LEAD")
        
        data = await MasterLeadController.GetByIdAndMasterDataId(lead.id, companyId, masterData.id)

        return data
    
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
        
        lead = await MasterLeadController.GetByIdAndMasterDataId(
            id,
            companyId,
            masterData.id
        )
        
        #check sales id 

        if not await LeadRepository.UpdateByUser(
            lead.id,
            {
                "isDeleted": True
            },
            updatedBy,
            datetime.now(timezone.utc)
        ):
            raise MsHTTPInternalServerErrorException("FAILED_UPDATE_LEAD")
        
        data = await LeadRepository.GetByIdAndMasterDataId(lead.id, masterData.id, ignoreDeleted=True)

        return data