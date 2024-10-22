from datetime import datetime
import re
from typing import Any
from controller.controllerUoM import UoMController
from controller.controllerUoMCategory import UoMCategoryController
from models.shared.modelEnvironment import MsEnvironment
from mongodb.mongoCollection import TbGenericMaterial
from models.generic_material.modelGenericMaterial import GenericMaterialCreateCommandRequest, GenericMaterialCreateWebRequest, GenericMaterialView
from models.shared.modelDataType import ObjectId
from models.shared.modelPagination import MsPagination, MsPaginationResult
from mongodb.mongoIndex import index_generic_material
from repositories.repoGenericMaterial import GenericMaterialRepository
from utils.util_http_exception import MsHTTPConflictException, MsHTTPInternalServerErrorException, MsHTTPNotFoundException
from utils.util_http_response import MsHTTPExceptionMessage, MsHTTPExceptionType
from utils.util_pagination import Paginate
from config.config import settings


class GenericMaterialController:
    @staticmethod
    async def Find(
        name: str | None,
        categoryId: ObjectId | None,
        companyId: ObjectId,
        paging: MsPagination
    ) -> MsPaginationResult[GenericMaterialView]:
        query: dict[str, Any] = {
                "isDeleted": False,
                "companyId": companyId
            }
        query.update({
            "name": {"$regex": re.compile(re.escape(name.strip()), re.IGNORECASE)} 
            if name and name.strip() else None,
            "categoryId": categoryId if categoryId is not None else None,
        })

        print(query)

        # Paginate and return results
        data = await Paginate(
            collection=TbGenericMaterial,
            query_filter=query,
            params=paging,
            session=None,
            hint=index_generic_material.isDeleted_companyId_name_categoryId.value.indexName,
            filterItem=True,
            resultItemsClass=GenericMaterialView,
            explain=True if settings.project.environment == MsEnvironment.development else False
        )

        return data
        
    @staticmethod
    async def Combo(
        name: str | None,
        categoryId: ObjectId | None,
        companyId: ObjectId
    ):
        data = await GenericMaterialRepository.Combo(
            name,
            categoryId,
            companyId
        )

        return data
        
    @staticmethod
    async def GetById(
        id: ObjectId,
    ):
        
        data = await GenericMaterialRepository.GetById(
            id
        )
        if data is None:
            raise MsHTTPNotFoundException(MsHTTPExceptionType.NOT_FOUND, MsHTTPExceptionMessage.GENERIC_MATERIAL_NOT_FOUND)
        
        return data
    
    @staticmethod
    async def GetByIdAndCompanyId(
        id: ObjectId,
        companyId: ObjectId
    ):
        data = await GenericMaterialRepository.GetByIdAndCompanyId(
            id, companyId
        )
        if data is None:
            raise MsHTTPNotFoundException(MsHTTPExceptionType.NOT_FOUND, MsHTTPExceptionMessage.GENERIC_MATERIAL_NOT_FOUND)
        
        return data

    @staticmethod
    async def Create(
        companyId: ObjectId,
        request: GenericMaterialCreateWebRequest,
        createdTime: datetime,
        createdBy: ObjectId
    ):
        if await GenericMaterialRepository.NameExists(
            request.name,
            companyId
        ):
            raise MsHTTPConflictException(
                MsHTTPExceptionType.GENERIC_MATERIAL_NAME_ALREADY_EXISTS, 
                MsHTTPExceptionMessage.GENERIC_MATERIAL_NAME_ALREADY_EXISTS_F.value.format(name=request.name)
                )
        
        category = await UoMCategoryController.GetByIdAndCompanyId(
            request.categoryId, companyId
        )
        uom = await UoMController.GetByIdAndCompanyId(
            request.uomId, companyId
        )

        newId = await GenericMaterialRepository.Create(
            GenericMaterialCreateCommandRequest(
                name=request.name,
                categoryId=category.id,
                salesPrice=request.salesPrice,
                cost=request.cost,
                uomId=uom.id,
                companyId=companyId,
                createdTime= createdTime,
                createdBy=createdBy 
            ),
        )
        if not newId:
            raise MsHTTPInternalServerErrorException(
                type="FAILED_CREATE_GENERIC_MATERIAL"
            )
        return newId
    
    @staticmethod
    async def UpdateByIdAndCompanyId(
        id: ObjectId,
        request: GenericMaterialCreateWebRequest,
        companyId: ObjectId,
        updatedTime: datetime,
        updatedBy: ObjectId
    ): 
        data = await GenericMaterialController.GetByIdAndCompanyId(
            id, companyId
        )
        if data.name == request.name: 
            return data

        if await GenericMaterialRepository.NameExists(
            request.name,
            companyId
        ):
            raise MsHTTPConflictException(
                MsHTTPExceptionType.GENERIC_MATERIAL_NAME_ALREADY_EXISTS, 
                MsHTTPExceptionMessage.GENERIC_MATERIAL_NAME_ALREADY_EXISTS_F.value.format(name=request.name)
                )
        
        category = await UoMCategoryController.GetByIdAndCompanyId(
            request.categoryId, companyId
        )
        uom = await UoMController.GetByIdAndCompanyId(
            request.uomId, companyId
        )
        
        if not await GenericMaterialRepository.UpdateByUser(
            data.id,
            {
                "name" : request.name,
                "categoryId":category.id,
                "salesPrice":request.salesPrice,
                "cost":request.cost,
                "uomId":uom.id
            },
            updatedBy,
            updatedTime
        ): 
            raise MsHTTPInternalServerErrorException(
                "FAILED_UPDATE_GENERIC_MATERIAL",
                "Gagal mengubah  Generic Material"
            )
        
        updatedData = await GenericMaterialController.GetByIdAndCompanyId(data.id, companyId)

        return updatedData
    

    @staticmethod
    async def Delete(
        id: ObjectId,
        companyId: ObjectId,
        updatedTime: datetime,
        updatedBy: ObjectId
    ): 
        data = await GenericMaterialController.GetByIdAndCompanyId(
            id,
            companyId
        )

        if not await GenericMaterialRepository.UpdateByUser(
            data.id,
            {
                "isDeleted" : True
            },
            updatedBy,
            updatedTime
        ): 
            raise MsHTTPInternalServerErrorException(
                "FAILED_DELETE_GENERIC_MATERIAL",
                "Gagal menghapus Generic Material"
            )
        
        deletedData = await GenericMaterialRepository.GetByIdAndCompanyId(
            id,
            companyId,
            ignoreDeleted=True
        )
        
        return deletedData