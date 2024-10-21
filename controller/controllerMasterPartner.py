from datetime import datetime, timezone
import re
from typing import Any
from pymongo.read_concern import ReadConcern
from pymongo.read_preferences import ReadPreference
from pymongo.write_concern import WriteConcern
from classes.classMongoDb import TMongoClientSession
from controller.controllerMasterData import MasterDataController
from controller.controllerMasterDataFollower import MasterDataFollowerController
from models.master_data_follower.enumMasterData import MasterDataFollowerStatus
from models.partner.enumPartnerType import PartnerType
from models.partner.modelPartner import PartnerCreateCommandRequest, PartnerCreateWebRequest, PartnerUpdateWebRequest, PartnerView
from models.shared.modelDataType import ObjectId
from models.shared.modelEnvironment import MsEnvironment
from models.shared.modelPagination import MsPagination
from mongodb.mongoClient import MongoDbStartDefaultSession
from mongodb.mongoCollection import TbPartner
from mongodb.mongoIndex import index_partner
from repositories.repoPartner import PartnerRepository
from utils.util_http_exception import MsHTTPBadRequestException, MsHTTPConflictException, MsHTTPInternalServerErrorException, MsHTTPNotFoundException
from utils.util_http_response import MsHTTPExceptionMessage, MsHTTPExceptionType
from utils.util_pagination import Paginate
from config.config import settings
from helpers.helperConfigFollower import CheckConfigFollower

class MasterPartnerController:

    @staticmethod
    async def Find(
        masterDataId: ObjectId,
        name: str | None,
        type: PartnerType | None,
        parentId: ObjectId | None,
        tags: list[str] | None,
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

        query.update({
            "name": {"$regex": re.compile(re.escape(name.strip()), re.IGNORECASE)} 
            if name and name.strip() else None,
            "type": type if type is not None else None,
            "parentId": parentId if parentId is not None else None,
            "tags": {"$all": tags} if tags else None
        })

        # Remove None values from the query
        query = {k: v for k, v in query.items() if v is not None}

        print(query)

        # Paginate and return results
        data = await Paginate(
            collection=TbPartner,
            query_filter=query,
            params=paging,
            session=None,
            hint=index_partner.isDeleted_masterDataId_name_type_parentId.value.indexName,
            filterItem=True,
            resultItemsClass=PartnerView,
            explain=True if settings.project.environment == MsEnvironment.development else False
        )

        return data

    @staticmethod
    async def FindByConfig(
        followerId: ObjectId,
        name: str | None,
        type: PartnerType | None,
        parentId: ObjectId | None,
        tags: list[str] | None,
        companyId: ObjectId,
        paging: MsPagination
    ):
        masterDataFollower = await MasterDataFollowerController.GetByIdAndStatus(
            followerId,
            MasterDataFollowerStatus.APPROVE
        )

        operations = CheckConfigFollower.checkConfigPartner(masterDataFollower, "PARTNER", "READ")        

        if operations == "":
            raise MsHTTPNotFoundException(MsHTTPExceptionType.NOT_FOUND, MsHTTPExceptionMessage.STATUS_NOT_MATCH)
        
        if operations == 0:
            query: dict[str, Any] = {
                "isDeleted": False,
                "masterDataId": masterDataFollower.masterDataId,
                "companyId": companyId
            }
        else:
            query: dict[str, Any] = {
                "isDeleted": False,
                "masterDataId": masterDataFollower.masterDataId,
            }

        query.update({
            "name": {"$regex": re.compile(re.escape(name.strip()), re.IGNORECASE)} 
            if name and name.strip() else None,
            "type": type if type is not None else None,
            "parentId": parentId if parentId is not None else None,
            "tags": {"$all": tags} if tags else None
        })

        # Remove None values from the query
        query = {k: v for k, v in query.items() if v is not None}
        
        data = await Paginate(
            collection=TbPartner,
            query_filter=query,
            params=paging,
            session=None,
            hint=index_partner.isDeleted_masterDataId_name_type_parentId.value.indexName,
            filterItem=True,
            resultItemsClass=PartnerView,
            explain=True if settings.project.environment == MsEnvironment.development else False
        )

        return data 

    @staticmethod
    async def GetById(
        id: ObjectId,
        companyId: ObjectId
    ):
        data= await PartnerRepository.GetByIdAndCompanyId(
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
        data = await PartnerRepository.GetByIdAndMasterDataId(
            id,
            masterData.id,
            session=session
        )
        if data is None:
            raise MsHTTPNotFoundException(MsHTTPExceptionType.NOT_FOUND,MsHTTPExceptionMessage.PARTNER_NOT_FOUND)
        
        return data
    
    @staticmethod
    async def GetByIdAndCompanyIdAndMasterDataId(
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
        data = await PartnerRepository.GetByIdAndCompanyIdAndMasterDataId(
            id,
            companyId,
            masterData.id,
            session=session
        )
        if data is None:
            raise MsHTTPNotFoundException(MsHTTPExceptionType.NOT_FOUND,MsHTTPExceptionMessage.PARTNER_NOT_FOUND)
        
        return data
    
    @staticmethod
    async def GetByIdAndCompanyIdAndMasterDataIdAndType(
        id: ObjectId,
        companyId: ObjectId,
        masterDataId: ObjectId,
        type: PartnerType,
        *,
        session: TMongoClientSession | None = None
    ):
        
        masterData = await MasterDataController.GetByIdAndCompanyId(
            masterDataId,
            companyId,
            session=session
        )
        data = await PartnerRepository.GetByIdAndCompanyIdAndMasterDataIdAndType(
            id,
            companyId,
            masterData.id,
            type,
            session=session
        )
        if data is None:
            raise MsHTTPNotFoundException(MsHTTPExceptionType.NOT_FOUND,MsHTTPExceptionMessage.PARTNER_NOT_FOUND)
        
        return data

    @staticmethod
    async def CheckValidParent(
        parentType: PartnerType,
        currentType: PartnerType
    ):
        if currentType is PartnerType.CABANG:
            return parentType is PartnerType.WILAYAH
        elif currentType is PartnerType.WILAYAH:
            return parentType is PartnerType.PUSAT
        return False  

    @staticmethod
    async def Create(
        companyId: ObjectId,
        masterDataId: ObjectId,
        request: PartnerCreateWebRequest,
        createdBy: ObjectId
    ):
    
        async def _coro(
            session: TMongoClientSession
        ):            
            masterData = await MasterDataController.GetByIdAndCompanyId(
                masterDataId,
                companyId,
                session=session
            )
            if await PartnerRepository.NameExists(
                request.name,
                masterData.id,
                session=session
            ):
                raise MsHTTPConflictException(
                    MsHTTPExceptionType.PARTNER_NAME_ALREADY_EXISTS, 
                    MsHTTPExceptionMessage.PARTNER_NAME_ALREADY_EXISTS_F.value.format(name=request.name)
                    )
            parent = None
            parentId = None
            if request.type != PartnerType.PUSAT:
                if request.parentId is None :
                    raise MsHTTPBadRequestException("PARENT_ID_REQUEIRED", "Tipe Partner selain pusat membutuhkan parentId")
                
                parent = await MasterPartnerController.GetByIdAndMasterDataId(
                        request.parentId,
                        companyId,
                        masterDataId,
                        session=session
                    )
            
                if not await MasterPartnerController.CheckValidParent(
                    parent.type, 
                    request.type
                ):
                    raise MsHTTPBadRequestException(
                        type="INVALID_PARENT_TYPE",
                        message="Tipe Partner tidak sesuai dengan Tipe Parent"
                    )
                parentId = parent.id
            
            
            newPartnerId = await PartnerRepository.Create(
                PartnerCreateCommandRequest(
                    name=request.name,
                    type=request.type,
                    tags=request.tags,
                    parentId=parentId,
                    masterDataId=masterDataId,
                    companyId=companyId,
                    createdTime=datetime.now(timezone.utc),
                    createdBy=createdBy
                ),
                session=session
            )
        
            if not newPartnerId:
                raise MsHTTPInternalServerErrorException("FAILED_CREATE_PARTNER")

            newPartner = await MasterPartnerController.GetByIdAndMasterDataId(
                newPartnerId,
                companyId,
                masterDataId,
                session=session
            )
            if parent: 
                childIds = parent.childIds
                childIds.append(newPartnerId)               
                if not await PartnerRepository.Update(
                    parent.id,
                    {
                        "childIds": childIds
                    },
                    session=session
                ):
                    raise MsHTTPInternalServerErrorException(
                        type="FAILED_TO_UPDATE_PARENT'S_CHILD",
                        message="Gagal update Parent"
                    )
            return newPartner
        
        async with await MongoDbStartDefaultSession() as session:
            ret: PartnerView = await session.with_transaction(
                lambda s: _coro(s),  # type: ignore
                read_concern=ReadConcern("snapshot"),
                write_concern=WriteConcern(w="majority", wtimeout=1000),
                read_preference=ReadPreference.PRIMARY
            )
            return ret
    
    @staticmethod
    async def UpdateByIdAndCompanyIdAndMasterDataId(
        id: ObjectId,
        companyId: ObjectId,
        masterDataId: ObjectId,
        request: PartnerUpdateWebRequest,
        updatedBy: ObjectId
    ):
        async def _coro(
            session: TMongoClientSession
        ):
            masterData = await MasterDataController.GetByIdAndCompanyId(
                masterDataId,
                companyId,
                session=session
            )
            partner = await MasterPartnerController.GetByIdAndMasterDataId(
                id,
                companyId,
                masterData.id,
                session=session
            )

            if partner.name != request.name and await PartnerRepository.NameExists(
                request.name,
                masterData.id,
                session=session
            ):
                raise MsHTTPConflictException(
                    MsHTTPExceptionType.PARTNER_NAME_ALREADY_EXISTS, 
                    MsHTTPExceptionMessage.PARTNER_NAME_ALREADY_EXISTS_F.value.format(name=request.name)
                )
            
            oldParent, newParent = None, None

            if partner.type != PartnerType.PUSAT:
                if not request.parentId:
                    raise MsHTTPBadRequestException("PARENT_ID_REQUEIRED", "Tipe Partner selain pusat membutuhkan parentId")
                if partner.parentId:
                    oldParent= await MasterPartnerController.GetByIdAndMasterDataId(
                        partner.parentId,
                        companyId,
                        masterDataId,
                        session=session
                    )
                newParent = await MasterPartnerController.GetByIdAndMasterDataId(
                        request.parentId,
                        companyId,
                        masterDataId,
                        session=session
                    )
                if not await MasterPartnerController.CheckValidParent(newParent.type, partner.type):
                    raise MsHTTPBadRequestException(
                        type="INVALID_PARENT_TYPE",
                        message="Tipe Partner tidak sesuai dengan Tipe Parent"
                    )
            

            if not await PartnerRepository.Update(
                partner.id,
                {
                    "name": request.name,
                    "parentId": request.parentId,
                    "tags": request.tags,
                    "updatedBy": updatedBy,
                    "updatedTime":datetime.now(timezone.utc).replace(tzinfo=None)
                },
                session=session
            ):
                raise MsHTTPInternalServerErrorException(
                    type="UPDATE_PARTNER_FAILED",
                    message="Gagal mengupdate Partner"
                )
            
            #updateOldParent
            if oldParent:
                childIds = oldParent.childIds
                childIds.remove(partner.id) 
                await PartnerRepository.UpdateByUser(
                    oldParent.id,
                    {
                        "childIds": childIds
                    },
                    updatedBy,
                    datetime.now(timezone.utc).replace(tzinfo=None),
                    session=session
                )
            #updateNewParent
            if newParent:
                childIds = newParent.childIds
                childIds.append(partner.id)   
                await PartnerRepository.UpdateByUser(
                    newParent.id,
                    {
                        "childIds": childIds
                    },
                    updatedBy,
                    datetime.now(timezone.utc).replace(tzinfo=None),
                    session=session
                )

            updatedPartner = await MasterPartnerController.GetByIdAndMasterDataId(
                id,
                companyId,
                masterDataId,
                session=session)
            
            return updatedPartner
        
        async with await MongoDbStartDefaultSession() as session:
            ret: PartnerView = await session.with_transaction(
                lambda s: _coro(s),  # type: ignore
                read_concern=ReadConcern("snapshot"),
                write_concern=WriteConcern(w="majority", wtimeout=1000),
                read_preference=ReadPreference.PRIMARY
            )
            return ret
        
    @staticmethod
    async def Delete(
        id: ObjectId,
        companyId: ObjectId,
        masterDataId: ObjectId,
        updatedBy: ObjectId
    ):
        async def _coro(
            session: TMongoClientSession
        ):
            masterData = await MasterDataController.GetByIdAndCompanyId(
                masterDataId,
                companyId,
                session=session
            )
            partner = await MasterPartnerController.GetByIdAndMasterDataId(
                id,
                companyId,
                masterData.id,
                session=session
            )
            if partner.childIds != []:
                raise MsHTTPConflictException(
                    "DELETE_PARTNER_FAILED",
                    "Partner masih memiliki child"
                )
            
            oldParent = None
            if partner.type != PartnerType.PUSAT:
                if partner.parentId:
                    oldParent= await MasterPartnerController.GetByIdAndMasterDataId(
                        partner.parentId,
                        companyId,
                        masterDataId,
                        session=session
                    )

            if not await PartnerRepository.UpdateByUser(
                id,
                {
                    "isDeleted": True
                },
                updatedBy,
                datetime.now(timezone.utc),
                session=session
            ):
                raise MsHTTPInternalServerErrorException(
                "FAILED_DELETE_PARTNER",
                "Gagal menghapus Partner"
            )

            #updateOldParent
            if oldParent:
                childIds = oldParent.childIds
                childIds.remove(partner.id)
                await PartnerRepository.UpdateByUser(
                    oldParent.id,
                    {
                        "childIds": childIds
                    },
                    updatedBy,
                    datetime.now(timezone.utc).replace(tzinfo=None),
                    session=session
                )

            deletedData = await PartnerRepository.GetByIdAndMasterDataId(
                id,
                masterData.id,
                ignoreDeleted=True
            )
            return deletedData
        
        async with await MongoDbStartDefaultSession() as session:
            ret: PartnerView = await session.with_transaction(
                lambda s: _coro(s),  # type: ignore
                read_concern=ReadConcern("snapshot"),
                write_concern=WriteConcern(w="majority", wtimeout=1000),
                read_preference=ReadPreference.PRIMARY
            )
            return ret