from uuid import UUID
from fastapi import HTTPException
from adapters.retailer_adapters import RetailerDataAdapter
from adapters.common_adapters import CommonAdapters
from managers.retailer_manager import RetailerManager
from models.retailer_model import (
    RetailerCreateModel,
    RetailerDatabaseModel,
    RetailerInboundCreateModel,
    RetailerInboundSearchModel,
    RetailerInboundUpdateModel,
    RetailerModel,
    RetailerOutboundModel,
    RetailerSearchModel,
    RetailerUpdateModel,
)
from models.common_model import (
    ItemList,
    OutboundItemListResponse,
    OutboundResultantPagingModel,
)
from util.database import PagingModel


dblist: list[RetailerDatabaseModel] = []

adapter: RetailerDataAdapter = RetailerDataAdapter()
common_adapter: CommonAdapters = CommonAdapters()
manager: RetailerManager = RetailerManager()


class RetailerController:
    def create(
        self, inbound_model: RetailerInboundCreateModel
    ) -> RetailerOutboundModel | None:
        model: RetailerCreateModel = (
            adapter.convert_from_inbound_create_model_to_create_model(
                inbound_model
            )
        )

        result = manager.create(model)

        if result is None:
            raise Exception('Received no model from create operation.')

        response_model: RetailerOutboundModel = (
            adapter.convert_from_model_to_outbound_model(result)
        )

        return response_model

    def get_by_id(self, id: UUID) -> RetailerOutboundModel | None:

        result = manager.get_by_id(id)

        if result is None:
            raise HTTPException(
                status_code=404, detail=f'Retailer with id {id} not found.'
            )

        response_model: RetailerOutboundModel = (
            adapter.convert_from_model_to_outbound_model(result)
        )

        return response_model

    def search(
        self, inbound_model: RetailerInboundSearchModel
    ) -> OutboundItemListResponse[RetailerOutboundModel]:

        paging_model: PagingModel = (
            common_adapter.convert_from_paged_inbound_model_to_paging_model(
                inbound_model
            )
        )

        search_model: RetailerSearchModel = (
            adapter.convert_from_inbound_search_model_to_search_model(
                inbound_model
            )
        )

        results: ItemList[RetailerModel] = manager.search(
            search_model, paging_model
        )

        return_result_list = list(
            map(
                lambda x: adapter.convert_from_model_to_outbound_model(x),
                results.items,
            )
        )

        outbound_paging: OutboundResultantPagingModel = (
            common_adapter.convert_from_paging_model_to_outbound_paging_model(
                results.paging
            )
        )

        return_result = OutboundItemListResponse(
            items=return_result_list, paging=outbound_paging
        )

        return return_result

    def update(
        self,
        id: UUID,
        inbound_model: RetailerInboundUpdateModel,
        explicitNullSet: list[str] | None = None,
    ):

        explicitNullSet = explicitNullSet or []

        model: RetailerUpdateModel = (
            adapter.convert_from_inbound_update_model_to_create_model(
                inbound_model
            )
        )

        result: None | RetailerModel = manager.update(id, model)

        if result is None:
            raise HTTPException(
                status_code=404, detail=f'Retailer with id {id} not found.'
            )

        response_model: RetailerOutboundModel = (
            adapter.convert_from_model_to_outbound_model(result)
        )

        return response_model

    def delete(self, id: UUID):

        result = manager.delete(id)

        if result is None:
            raise HTTPException(
                status_code=404, detail=f'Retailer with id {id} not found.'
            )

        response_model: RetailerOutboundModel = (
            adapter.convert_from_model_to_outbound_model(result)
        )

        return response_model
