from datetime import datetime
import re
from typing import Any
from models.shared.modelEnvironment import MsEnvironment
from mongodb.mongoCollection import TbGenericMaterialCategory
from models.generic_material.modelGenericMaterialCategory import GenericMaterialCategoryCreateCommandRequest, GenericMaterialCategoryCreateWebRequest, GenericMaterialCategoryView
from models.shared.modelDataType import ObjectId
from models.shared.modelPagination import MsPagination, MsPaginationResult
from mongodb.mongoIndex import index_generic_material_category
from repositories.repoGenericMaterialCategory import GenericMaterialCategoryRepository
from utils.util_http_exception import MsHTTPConflictException, MsHTTPInternalServerErrorException, MsHTTPNotFoundException
from utils.util_http_response import MsHTTPExceptionMessage, MsHTTPExceptionType
from utils.util_pagination import Paginate
from config.config import settings


class GenericMaterialCategoryController:
    @staticmethod
    async def Find(
        name: str | None,
        companyId: ObjectId,
        paging: MsPagination
    ) -> MsPaginationResult[GenericMaterialCategoryView]:
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
            collection=TbGenericMaterialCategory,
            query_filter=query,
            params=paging,
            session=None,
            hint=index_generic_material_category.isDeleted_companyId_name.value.indexName,
            filterItem=True,
            resultItemsClass=GenericMaterialCategoryView,
            explain=True if settings.project.environment == MsEnvironment.development else False
        )

        return data
        
    @staticmethod
    async def Combo(
        name: str | None,
        companyId: ObjectId
    ):
        data = await GenericMaterialCategoryRepository.Combo(
            name,
            companyId
        )

        return data
        
    @staticmethod
    async def GetById(
        id: ObjectId,
    ):
        
        data = await GenericMaterialCategoryRepository.GetById(
            id
        )

        if data is None:
            raise MsHTTPNotFoundException(MsHTTPExceptionType.NOT_FOUND, MsHTTPExceptionMessage.GENERIC_MATERIAL_CATEGORY_NOT_FOUND)
        
        return data
    
    @staticmethod
    async def GetByIdAndCompanyId(
        id: ObjectId,
        companyId: ObjectId
    ):
        data = await GenericMaterialCategoryRepository.GetByIdAndCompanyId(
            id, companyId
        )
        if data is None:
            raise MsHTTPNotFoundException(MsHTTPExceptionType.NOT_FOUND, MsHTTPExceptionMessage.GENERIC_MATERIAL_CATEGORY_NOT_FOUND)
        
        return data

    @staticmethod
    async def Create(
        companyId: ObjectId,
        request: GenericMaterialCategoryCreateWebRequest,
        createdTime: datetime,
        createdBy: ObjectId
    ):
        if await GenericMaterialCategoryRepository.NameExists(
            request.name,
            companyId
        ):
            raise MsHTTPConflictException(
                MsHTTPExceptionType.GENERIC_MATERIAL_CATEGORY_NAME_ALREADY_EXISTS, 
                MsHTTPExceptionMessage.GENERIC_MATERIAL_CATEGORY_NAME_ALREADY_EXISTS_F.value.format(name=request.name)
                )
        newId = await GenericMaterialCategoryRepository.Create(
            GenericMaterialCategoryCreateCommandRequest(
                name=request.name,
                companyId=companyId,
                createdTime= createdTime,
                createdBy=createdBy 
            ),
        )
        if not newId:
            raise MsHTTPInternalServerErrorException(
                type="FAILED_CREATE_GENERIC_MATERIAL_CATEGORY"
            )
        return newId
    
    @staticmethod
    async def UpdateByIdAndCompanyId(
        id: ObjectId,
        request: GenericMaterialCategoryCreateWebRequest,
        companyId: ObjectId,
        updatedTime: datetime,
        updatedBy: ObjectId
    ): 
        data = await GenericMaterialCategoryController.GetByIdAndCompanyId(
            id, companyId
        )
        if data.name == request.name: 
            return data

        if await GenericMaterialCategoryRepository.NameExists(
            request.name,companyId
        ):
            raise MsHTTPConflictException(
                MsHTTPExceptionType.GENERIC_MATERIAL_CATEGORY_NAME_ALREADY_EXISTS, 
                MsHTTPExceptionMessage.GENERIC_MATERIAL_CATEGORY_NAME_ALREADY_EXISTS_F.value.format(name=request.name)
                )

        if not await GenericMaterialCategoryRepository.UpdateByUser(
            data.id,
            {
                "name" : request.name
            },
            updatedBy,
            updatedTime
        ): 
            raise MsHTTPInternalServerErrorException(
                "FAILED_UPDATE_GENERIC_MATERIAL_CATEGORY",
                "Gagal mengubah Kategori Generic Material"
            )
        
        updatedData = await GenericMaterialCategoryController.GetByIdAndCompanyId(data.id, companyId)

        return updatedData
    

    @staticmethod
    async def Delete(
        id: ObjectId,
        companyId: ObjectId,
        updatedTime: datetime,
        updatedBy: ObjectId
    ): 
        data = await GenericMaterialCategoryController.GetByIdAndCompanyId(
            id,
            companyId
        )

        if not await GenericMaterialCategoryRepository.UpdateByUser(
            data.id,
            {
                "isDeleted" : True
            },
            updatedBy,
            updatedTime
        ): 
            raise MsHTTPInternalServerErrorException(
                "FAILED_DELETE_GENERIC_MATERIAL_CATEGORY",
                "Gagal menghapus Kategori Generic Material"
            )
        
        deletedData = await GenericMaterialCategoryRepository.GetByIdAndCompanyId(
            id,
            companyId,
            ignoreDeleted=True
        )
        
        return deletedData