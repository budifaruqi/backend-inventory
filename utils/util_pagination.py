import json
from typing import Any
from fastapi.encoders import jsonable_encoder
import pymongo
from classes.classMongoDb import TMongoClientSession, TMongoCollection
from models.shared.modelPagination import MsPagination, MsPagination2, MsPaginationResult, MsPaginationResult2, QuerySortingOrder, TGenericPaginationModel
from utils.util_logger import msLogger


async def Paginate(
    collection: TMongoCollection,
    query_filter: dict[str, Any],
    params: MsPagination,
    resultItemsClass: type[TGenericPaginationModel],
    session: TMongoClientSession | None = None,
    hint: str | None = None,
    filterItem: bool = True,
    explain: bool = False,
    **kwargs: Any
) -> MsPaginationResult[TGenericPaginationModel]:
    """
    - Http method GET
    - Single sorting field. if one of `sortby` or `order` is null, sorting query ignored
    """
    
    if params.page == 1:
        total = await collection.count_documents(query_filter)
    else:
        total = -1
    offset = params.size * (params.page - 1)
    cursor = collection.find(
        query_filter,
        resultItemsClass.Projection() if filterItem else {},
        skip=offset,
        limit=params.size,
        session=session,
        hint=hint,
        **kwargs
    )
    if (params.sortby is not None) and (len(params.sortby) > 0):
        cursor.sort(params.sortby, pymongo.ASCENDING if params.order == QuerySortingOrder.Ascending else pymongo.DESCENDING)
    items: list[dict[str, Any]] = await cursor.to_list(length=params.size) # type: ignore

    if explain:
        try:
            explained: Any = await cursor.explain()
            msLogger.data("pagination explain: \n" + json.dumps(jsonable_encoder(explained), indent=2))
        except Exception as err:
            msLogger.critical("Error process mongo explain")
            msLogger.critical(str(err))

    return MsPaginationResult[resultItemsClass](
        sortby=params.sortby,
        size=params.size,
        page=params.page,
        order=params.order,
        total=total,
        items=[resultItemsClass(**item) for item in items]
    )

async def Paginate2(
    collection: TMongoCollection,
    query_filter: dict[str, Any],
    params: MsPagination2,
    resultItemsClass: type[TGenericPaginationModel],
    session: TMongoClientSession | None = None,
    hint: str | None = None,
    filterItem: bool = True,
    explain: bool = False,
    **kwargs: Any
) -> MsPaginationResult2[TGenericPaginationModel]:
    """
    - Http method POST/PUT
    - Allow multiple sorting condition
    """
    
    if params.page == 1:
        total = await collection.count_documents(query_filter)
    else:
        total = -1
    offset = params.size * (params.page - 1)
    cursor = collection.find(
        query_filter,
        resultItemsClass.Projection() if filterItem else {},
        skip=offset,
        limit=params.size,
        session=session,
        hint=hint,
        **kwargs
    )
    if (params.sort is not None) and (len(params.sort) > 0):
        i = 0
        while i < len(params.sort):
            sort = params.sort[i]
            sort.sortby = sort.sortby.strip()
            if len(sort.sortby) == 0:
                params.sort.pop(i)
                continue
            
            params.sort[i] = sort
            i += 1

        if len(params.sort) > 0:
            sort = [(p.sortby, pymongo.ASCENDING if p.order == QuerySortingOrder.Ascending else pymongo.DESCENDING) for p in params.sort]
            cursor.sort(sort)
    items: list[dict[str, Any]] = await cursor.to_list(length=params.size) # type: ignore

    if explain:
        try:
            explained: Any = await cursor.explain()
            msLogger.data("pagination explain: \n" + json.dumps(jsonable_encoder(explained), indent=2))
        except Exception as err:
            msLogger.critical("Error process mongo explain")
            msLogger.critical(str(err))
    
    return MsPaginationResult2[resultItemsClass](
        sort=params.sort,
        size=params.size,
        page=params.page,
        total=total,
        items=[resultItemsClass(**item) for item in items]
    )