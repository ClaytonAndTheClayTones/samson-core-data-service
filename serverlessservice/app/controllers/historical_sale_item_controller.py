from copy import copy
from datetime import datetime
from uuid import UUID

from fastapi import HTTPException
from adapters.historical_sale_item_adapters import HistoricalSaleItemDataAdapter
from adapters.common_adapters import CommonAdapters
from managers.historical_sale_item_manager import HistoricalSaleItemManager
from models.historical_sale_item_model import (
    HistoricalSaleItemCreateModel,
    HistoricalSaleItemDatabaseModel,
    HistoricalSaleItemInboundCreateModel,
    HistoricalSaleItemInboundSearchModel, 
    HistoricalSaleItemModel,
    HistoricalSaleItemOutboundModel,
    HistoricalSaleItemSearchModel, 
)
from models.common_model import (
    ItemList,
    OutboundItemListResponse,
    OutboundResultantPagingModel,
)
from util.database import PagingModel
 
adapter: HistoricalSaleItemDataAdapter = HistoricalSaleItemDataAdapter()
common_adapter: CommonAdapters = CommonAdapters()
manager: HistoricalSaleItemManager = HistoricalSaleItemManager()


class HistoricalSaleItemController:

    def create(
        self, inbound_model: HistoricalSaleItemInboundCreateModel
    ) -> HistoricalSaleItemOutboundModel | None:
        model: HistoricalSaleItemCreateModel = (
            adapter.convert_from_inbound_create_model_to_create_model(
                inbound_model))

        result = manager.create(model)

        if result is None:
            raise Exception('Received no model from create operation.')

        response_model: HistoricalSaleItemOutboundModel = (
            adapter.convert_from_model_to_outbound_model(result))

        return response_model

    def get_by_id(self, id: UUID) -> HistoricalSaleItemOutboundModel | None:

        result = manager.get_by_id(id)

        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f'HistoricalSaleItem with id {id} not found.',
            )

        response_model: HistoricalSaleItemOutboundModel = (
            adapter.convert_from_model_to_outbound_model(result))

        return response_model

    def search(
        self, inbound_model: HistoricalSaleItemInboundSearchModel
    ) -> OutboundItemListResponse[HistoricalSaleItemOutboundModel]:

        paging_model: PagingModel = (
            common_adapter.convert_from_paged_inbound_model_to_paging_model(
                inbound_model))

        search_model: HistoricalSaleItemSearchModel = (
            adapter.convert_from_inbound_search_model_to_search_model(
                inbound_model))

        results: ItemList[HistoricalSaleItemModel] = manager.search(
            search_model, paging_model)

        return_result_list = list(
            map(
                lambda x: adapter.convert_from_model_to_outbound_model(x),
                results.items,
            ))

        outbound_paging: OutboundResultantPagingModel = (
            common_adapter.convert_from_paging_model_to_outbound_paging_model(
                results.paging))

        return_result = OutboundItemListResponse(items=return_result_list,
                                                 paging=outbound_paging)

        return return_result
 
    def delete(self, id: UUID):

        result = manager.delete(id)

        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f'HistoricalSaleItem with id {id} not found.',
            )

        response_model: HistoricalSaleItemOutboundModel = (
            adapter.convert_from_model_to_outbound_model(result))

        return response_model
