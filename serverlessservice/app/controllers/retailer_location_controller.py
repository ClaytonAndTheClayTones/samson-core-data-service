from copy import copy
from datetime import datetime
from uuid import UUID

from fastapi import HTTPException
from adapters.retailer_location_adapters import RetailerLocationDataAdapter
from adapters.common_adapters import CommonAdapters 
from managers.managers import Manager
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

from fastapi.datastructures import Headers

from util.database import PagingModel
 

adapter: RetailerLocationDataAdapter = RetailerLocationDataAdapter()
common_adapter: CommonAdapters = CommonAdapters()
manager: Manager = Manager()


class RetailerLocationController:
        
    def create(
        self, 
        inbound_model: RetailerLocationInboundCreateModel,
        headers: Headers
    ) -> RetailerLocationOutboundModel | None:
        
        request_operators = common_adapter.convert_from_headers_to_operators(headers)
        
        model: RetailerLocationCreateModel = adapter.convert_from_inbound_create_model_to_create_model(inbound_model)

        result = manager.create_retailer_location(model, request_operators)

        if result is None:
            raise Exception('Received no model from create operation.')

        response_model: RetailerLocationOutboundModel = adapter.convert_from_model_to_outbound_model(result)

        return response_model

    def get_by_id(
        self, 
        id: UUID, 
        headers: Headers
    ) -> RetailerLocationOutboundModel | None:
        
        request_operators = common_adapter.convert_from_headers_to_operators(headers)
        
        result = manager.get_retailer_location_by_id(id, request_operators)

        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f'RetailerLocation with id {id} not found.',
            )

        response_model: RetailerLocationOutboundModel = adapter.convert_from_model_to_outbound_model(result)

        return response_model

    def search(
        self, 
        inbound_model: RetailerLocationInboundSearchModel, 
        headers: Headers
    ) -> OutboundItemListResponse[RetailerLocationOutboundModel]:

        request_operators = common_adapter.convert_from_headers_to_operators(headers)
        
        paging_model: PagingModel = common_adapter.convert_from_paged_inbound_model_to_paging_model(inbound_model)

        search_model: RetailerLocationSearchModel = adapter.convert_from_inbound_search_model_to_search_model(inbound_model)

        results: ItemList[RetailerLocationModel] = manager.search_retailer_locations(
            search_model, 
            paging_model, 
            request_operators
        )

        return_result_list = list(
            map(
                lambda x: adapter.convert_from_model_to_outbound_model(x),
                results.items,
            )
        )

        outbound_paging: OutboundResultantPagingModel = common_adapter.convert_from_paging_model_to_outbound_paging_model(results.paging)

        return_result = OutboundItemListResponse(items=return_result_list, paging=outbound_paging)

        return return_result

    def update(
        self,
        id: UUID,
        inbound_model: RetailerLocationInboundUpdateModel, 
        headers: Headers
    ): 
        request_operators = common_adapter.convert_from_headers_to_operators(headers)

        model: RetailerLocationUpdateModel = (
            adapter.convert_from_inbound_update_model_to_create_model(
                inbound_model))

        result: None | RetailerLocationModel = manager.update_retailer_location(
            id, 
            model,
            None,
            request_operators
        )

        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f'RetailerLocation with id {id} not found.',
            )

        response_model: RetailerLocationOutboundModel = adapter.convert_from_model_to_outbound_model(result)

        return response_model

    def delete(
        self, 
        id: UUID, 
        headers: Headers
    ) -> RetailerLocationOutboundModel | None:

        request_operators = common_adapter.convert_from_headers_to_operators(headers)
        
        result = manager.delete_retailer_location(id, request_operators)

        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f'RetailerLocation with id {id} not found.',
            )

        response_model: RetailerLocationOutboundModel = adapter.convert_from_model_to_outbound_model(result)

        return response_model
