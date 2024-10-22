from datetime import datetime
import re
from typing import Any
from models.shared.modelDataType import ObjectId
from models.shared.modelEnvironment import MsEnvironment
from models.shared.modelPagination import MsPagination, MsPaginationResult
from models.uom.modelUoM import UoMBase
from models.uom.modelUoMCategory import UoMCategoryCreateCommandRequest, UoMCategoryCreateWebRequest, UoMCategoryView
from mongodb.mongoCollection import TbUomCategory, TbUom
from mongodb.mongoIndex import index_uom, index_uom_category
from repositories.repoUoMCategory import UoMCategoryRepository
from utils.util_http_exception import MsHTTPConflictException, MsHTTPInternalServerErrorException, MsHTTPNotFoundException
from utils.util_http_response import MsHTTPExceptionMessage, MsHTTPExceptionType
from utils.util_pagination import Paginate
from config.config import settings


class UoMCategoryController:
    @staticmethod
    async def Find(
        name: str | None,
        companyId: ObjectId,
        paging: MsPagination
    ) -> MsPaginationResult[UoMCategoryView]:
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
            collection=TbUomCategory,
            query_filter=query,
            params=paging,
            session=None,
            hint=index_uom_category.isDeleted_companyId_name.value.indexName,
            filterItem=True,
            resultItemsClass=UoMCategoryView,
            explain=True if settings.project.environment == MsEnvironment.development else False
        )

        for category in data.items:
            uomQuery:dict[str, Any] = {
                "companyId": companyId,
                "categoryId": category.id,
                "isDeleted": False
            }
            cursor = TbUom.find(
                        uomQuery,
                        UoMBase.Projection(), 
                        hint=index_uom.isDeleted_companyId_categoryId.value.indexName
                    )
            itemsRaw: list[dict[str, Any]] = await cursor.to_list(None) # type: ignore
            category.uoms = [UoMBase(**uom) for uom in itemsRaw] 

        return data
        
    @staticmethod
    async def Combo(
        name: str | None,
        companyId: ObjectId
    ):
        data = await UoMCategoryRepository.Combo(
            name,
            companyId
        )

        return data
        
    @staticmethod
    async def GetById(
        id: ObjectId,
    ):
        
        data = await UoMCategoryRepository.GetById(
            id
        )

        if data is None:
            raise MsHTTPNotFoundException(MsHTTPExceptionType.NOT_FOUND, MsHTTPExceptionMessage.UOM_CATEGORY_NOT_FOUND)
        
        return data
    
    @staticmethod
    async def GetByIdAndCompanyId(
        id: ObjectId,
        companyId: ObjectId
    ):
        data = await UoMCategoryRepository.GetByIdAndCompanyId(
            id, companyId
        )
        if data is None:
            raise MsHTTPNotFoundException(MsHTTPExceptionType.NOT_FOUND, "UOM_CATEGORY_NOT_FOUND")
        
        return data

    @staticmethod
    async def Create(
        companyId: ObjectId,
        request: UoMCategoryCreateWebRequest,
        createdTime: datetime,
        createdBy: ObjectId
    ):
        if await UoMCategoryRepository.NameExists(
            request.name,
            companyId
        ):
            raise MsHTTPConflictException(
                MsHTTPExceptionType.UOM_CATEGORY_NAME_ALREADY_EXISTS, 
                MsHTTPExceptionMessage.UOM_CATEGORY_NAME_ALREADY_EXISTS_F.value.format(name=request.name)
                )
        newMasterDataId = await UoMCategoryRepository.Create(
            UoMCategoryCreateCommandRequest(
                name=request.name,
                companyId=companyId,
                createdTime= createdTime,
                createdBy=createdBy 
            ),
        )
        if not newMasterDataId:
            raise MsHTTPInternalServerErrorException(
                type="FAILED_CREATE_UOM_CATEGORY"
            )
        return newMasterDataId
    
    @staticmethod
    async def UpdateByIdAndCompanyId(
        id: ObjectId,
        request: UoMCategoryCreateWebRequest,
        companyId: ObjectId,
        updatedTime: datetime,
        updatedBy: ObjectId
    ): 
        data = await UoMCategoryController.GetByIdAndCompanyId(
            id, companyId
        )
        if data.name == request.name: 
            return data

        if await UoMCategoryRepository.NameExists(
            request.name,companyId
        ):
            raise MsHTTPConflictException(
                MsHTTPExceptionType.UOM_CATEGORY_NAME_ALREADY_EXISTS, 
                MsHTTPExceptionMessage.UOM_CATEGORY_NAME_ALREADY_EXISTS_F.value.format(name=request.name)
                )

        if not await UoMCategoryRepository.UpdateByUser(
            data.id,
            {
                "name" : request.name
            },
            updatedBy,
            updatedTime
        ): 
            raise MsHTTPInternalServerErrorException(
                "FAILED_UPDATE_UOM_CATEGORY",
                "Gagal mengubah Kategori Unit Of Measure"
            )
        
        updatedData = await UoMCategoryController.GetByIdAndCompanyId(data.id, companyId)

        return updatedData
    

    @staticmethod
    async def Delete(
        id: ObjectId,
        companyId: ObjectId,
        updatedTime: datetime,
        updatedBy: ObjectId
    ): 
        data = await UoMCategoryController.GetByIdAndCompanyId(
            id,
            companyId
        )

        if not await UoMCategoryRepository.UpdateByUser(
            data.id,
            {
                "isDeleted" : True
            },
            updatedBy,
            updatedTime
        ): 
            raise MsHTTPInternalServerErrorException(
                "FAILED_DELETE_UOM_CATEGORY",
                "Gagal menghapus Kategori Unit of Measure"
            )
        
        deletedData = await UoMCategoryRepository.GetByIdAndCompanyId(
            id,
            companyId,
            ignoreDeleted=True
        )
        
        return deletedData