from copy import copy
from datetime import datetime
from uuid import UUID

from fastapi import HTTPException
from adapters.historical_sale_adapters import HistoricalSaleDataAdapter
from adapters.common_adapters import CommonAdapters
from managers.historical_sale_manager import HistoricalSaleManager
from models.historical_sale_model import (
    HistoricalSaleCreateModel,
    HistoricalSaleDatabaseModel,
    HistoricalSaleInboundCreateModel,
    HistoricalSaleInboundSearchModel, 
    HistoricalSaleModel,
    HistoricalSaleOutboundModel,
    HistoricalSaleSearchModel, 
)
from models.common_model import (
    ItemList,
    OutboundItemListResponse,
    OutboundResultantPagingModel,
)
from util.database import PagingModel
 
adapter: HistoricalSaleDataAdapter = HistoricalSaleDataAdapter()
common_adapter: CommonAdapters = CommonAdapters()
manager: HistoricalSaleManager = HistoricalSaleManager()


class HistoricalSaleController:

    def create(
        self, inbound_model: HistoricalSaleInboundCreateModel
    ) -> HistoricalSaleOutboundModel | None:
        model: HistoricalSaleCreateModel = (
            adapter.convert_from_inbound_create_model_to_create_model(
                inbound_model))

        result = manager.create(model)

        if result is None:
            raise Exception('Received no model from create operation.')

        response_model: HistoricalSaleOutboundModel = (
            adapter.convert_from_model_to_outbound_model(result))

        return response_model

    def get_by_id(self, id: UUID) -> HistoricalSaleOutboundModel | None:

        result = manager.get_by_id(id)

        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f'HistoricalSale with id {id} not found.',
            )

        response_model: HistoricalSaleOutboundModel = (
            adapter.convert_from_model_to_outbound_model(result))

        return response_model

    def search(
        self, inbound_model: HistoricalSaleInboundSearchModel
    ) -> OutboundItemListResponse[HistoricalSaleOutboundModel]:

        paging_model: PagingModel = (
            common_adapter.convert_from_paged_inbound_model_to_paging_model(
                inbound_model))

        search_model: HistoricalSaleSearchModel = (
            adapter.convert_from_inbound_search_model_to_search_model(
                inbound_model))

        results: ItemList[HistoricalSaleModel] = manager.search(
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
                detail=f'HistoricalSale with id {id} not found.',
            )

        response_model: HistoricalSaleOutboundModel = (
            adapter.convert_from_model_to_outbound_model(result))

        return response_model
