from copy import copy
from datetime import datetime
from uuid import UUID

from fastapi import HTTPException
from adapters.retailer_location_adapters import RetailerLocationDataAdapter
from adapters.common_adapters import CommonAdapters
from managers.retailer_location_manager import RetailerLocationManager
from models.retailer_location_model import (
    RetailerLocationCreateModel,
    RetailerLocationDatabaseModel,
    RetailerLocationInboundCreateModel,
    RetailerLocationInboundSearchModel,
    RetailerLocationInboundUpdateModel,
    RetailerLocationModel,
    RetailerLocationOutboundModel,
    RetailerLocationSearchModel,
    RetailerLocationUpdateModel,
)
from models.common_model import (
    ItemList,
    OutboundItemListResponse,
    OutboundResultantPagingModel,
)
from util.database import PagingModel
 

adapter: RetailerLocationDataAdapter = RetailerLocationDataAdapter()
common_adapter: CommonAdapters = CommonAdapters()
manager: RetailerLocationManager = RetailerLocationManager()


class RetailerLocationController:

    def create(
        self, inbound_model: RetailerLocationInboundCreateModel
    ) -> RetailerLocationOutboundModel | None:
        model: RetailerLocationCreateModel = (
            adapter.convert_from_inbound_create_model_to_create_model(
                inbound_model))

        result = manager.create(model)

        if result is None:
            raise Exception('Received no model from create operation.')

        response_model: RetailerLocationOutboundModel = (
            adapter.convert_from_model_to_outbound_model(result))

        return response_model

    def get_by_id(self, id: UUID) -> RetailerLocationOutboundModel | None:

        result = manager.get_by_id(id)

        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f'RetailerLocation with id {id} not found.',
            )

        response_model: RetailerLocationOutboundModel = (
            adapter.convert_from_model_to_outbound_model(result))

        return response_model

    def search(
        self, inbound_model: RetailerLocationInboundSearchModel
    ) -> OutboundItemListResponse[RetailerLocationOutboundModel]:

        paging_model: PagingModel = (
            common_adapter.convert_from_paged_inbound_model_to_paging_model(
                inbound_model))

        search_model: RetailerLocationSearchModel = (
            adapter.convert_from_inbound_search_model_to_search_model(
                inbound_model))

        results: ItemList[RetailerLocationModel] = manager.search(
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

    def update(
        self,
        id: UUID,
        inbound_model: RetailerLocationInboundUpdateModel,
        explicitNullSet: list[str] | None = None,
    ):

        explicitNullSet = explicitNullSet or []

        model: RetailerLocationUpdateModel = (
            adapter.convert_from_inbound_update_model_to_create_model(
                inbound_model))

        result: None | RetailerLocationModel = manager.update(id, model)

        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f'RetailerLocation with id {id} not found.',
            )

        response_model: RetailerLocationOutboundModel = (
            adapter.convert_from_model_to_outbound_model(result))

        return response_model

    def delete(self, id: UUID):

        result = manager.delete(id)

        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f'RetailerLocation with id {id} not found.',
            )

        response_model: RetailerLocationOutboundModel = (
            adapter.convert_from_model_to_outbound_model(result))

        return response_model
