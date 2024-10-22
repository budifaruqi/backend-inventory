from datetime import datetime
import re
from typing import Any
from models.shared.modelDataType import ObjectId
from models.shared.modelEnvironment import MsEnvironment
from models.shared.modelPagination import MsPagination
from models.uom.modelUoM import UoMCreateCommandRequest, UoMCreateWebRequest, UoMView
from mongodb.mongoCollection import TbUom
from mongodb.mongoIndex import index_uom
from repositories.repoUoM import UoMRepository
from utils.util_http_exception import MsHTTPConflictException, MsHTTPInternalServerErrorException, MsHTTPNotFoundException
from utils.util_http_response import MsHTTPExceptionMessage, MsHTTPExceptionType
from utils.util_pagination import Paginate
from config.config import settings

class UoMController:

    @staticmethod
    async def Find(
        name: str | None,
        categoryId: ObjectId | None,
        isActive: bool | None,
        companyId: ObjectId,
        paging: MsPagination
    ):
        query: dict[str, Any] = {
            "isDeleted": False,
            "companyId": companyId
        }
        query.update({
            "name": {"$regex": re.compile(re.escape(name.strip()), re.IGNORECASE)} 
            if name and name.strip() else None,
            "categoryId": categoryId if categoryId is not None else None,
            "isActive": isActive if isActive is not None else None
        })

        # Remove None values from the query
        query = {k: v for k, v in query.items() if v is not None}
        print(query)

        # Paginate and return results
        data = await Paginate(
            collection=TbUom,
            query_filter=query,
            params=paging,
            session=None,
            hint=index_uom.isDeleted_companyId_isActive_categoryId_name.value.indexName,
            filterItem=True,
            resultItemsClass=UoMView,
            explain=True if settings.project.environment == MsEnvironment.development else False
        )

        return data
    
    @staticmethod
    async def Combo(
        name: str | None,
        categoryId: ObjectId | None,
        isActive: bool | None,
        companyId: ObjectId
    ):
        data = await UoMRepository.Combo(
            name,
            categoryId,
            isActive,
            companyId
        )

        return data
        
    @staticmethod
    async def GetById(
        id: ObjectId,
    ):
        
        data = await UoMRepository.GetById(
            id
        )

        if data is None:
            raise MsHTTPNotFoundException(MsHTTPExceptionType.NOT_FOUND, MsHTTPExceptionMessage.UOM_NOT_FOUND)
        
        return data
    
    @staticmethod
    async def GetByIdAndCompanyId(
        id: ObjectId,
        companyId: ObjectId
    ):
        data = await UoMRepository.GetByIdAndCompanyId(
            id, companyId
        )
        if data is None:
            raise MsHTTPNotFoundException(MsHTTPExceptionType.NOT_FOUND, "UOM_NOT_FOUND")
        
        return data
    
    @staticmethod
    async def Create(
        companyId: ObjectId,
        request: UoMCreateWebRequest,
        createdTime: datetime,
        createdBy: ObjectId
    ):
        if await UoMRepository.NameExists(
            request.name,
            companyId
        ):
            raise MsHTTPConflictException(
                MsHTTPExceptionType.UOM_NAME_ALREADY_EXISTS, 
                MsHTTPExceptionMessage.UOM_NAME_ALREADY_EXISTS_F.value.format(name=request.name)
                )
        newId = await UoMRepository.Create(
            UoMCreateCommandRequest(
                name=request.name,
                categoryId=request.categoryId,
                type=request.type,
                ratio=request.ratio,
                isActive=request.isActive,
                companyId=companyId,
                createdTime= createdTime,
                createdBy=createdBy 
            ),
        )
        if not newId:
            raise MsHTTPInternalServerErrorException(
                type="FAILED_CREATE_UOM"
            )
        return newId
    
    @staticmethod
    async def UpdateByIdAndCompanyId(
        id: ObjectId,
        request: UoMCreateWebRequest,
        companyId: ObjectId,
        updatedTime: datetime,
        updatedBy: ObjectId
    ): 
        data = await UoMController.GetByIdAndCompanyId(
            id, companyId
        )
        if data.name == request.name: 
            return data

        if await UoMRepository.NameExists(
            request.name,companyId
        ):
            raise MsHTTPConflictException(
                MsHTTPExceptionType.UOM_NAME_ALREADY_EXISTS, 
                MsHTTPExceptionMessage.UOM_NAME_ALREADY_EXISTS_F.value.format(name=request.name)
                )

        if not await UoMRepository.UpdateByUser(
            data.id,
            {
                "name" : request.name
            },
            updatedBy,
            updatedTime
        ): 
            raise MsHTTPInternalServerErrorException(
                "FAILED_UPDATE_UOM_CATEGORY",
                "Gagal mengubah Unit Of Measure"
            )
        
        updatedData = await UoMController.GetByIdAndCompanyId(data.id, companyId)

        return updatedData
    

    @staticmethod
    async def Delete(
        id: ObjectId,
        companyId: ObjectId,
        updatedTime: datetime,
        updatedBy: ObjectId
    ): 
        data = await UoMController.GetByIdAndCompanyId(
            id,
            companyId
        )

        if not await UoMRepository.UpdateByUser(
            data.id,
            {
                "isDeleted" : True
            },
            updatedBy,
            updatedTime
        ): 
            raise MsHTTPInternalServerErrorException(
                "FAILED_DELETE_UOM",
                "Gagal menghapus Unit of Measure"
            )
        
        deletedData = await UoMRepository.GetByIdAndCompanyId(
            id,
            companyId,
            ignoreDeleted=True
        )
        
        return deletedData