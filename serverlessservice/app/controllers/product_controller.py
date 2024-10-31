from copy import copy
from datetime import datetime
from uuid import UUID

from fastapi import HTTPException
from adapters.product_adapters import ProductDataAdapter
from adapters.common_adapters import CommonAdapters
from managers.product_manager import ProductManager
from models.product_model import (
    ProductCreateModel,
    ProductDatabaseModel,
    ProductInboundCreateModel,
    ProductInboundSearchModel,
    ProductInboundUpdateModel,
    ProductModel,
    ProductOutboundModel,
    ProductSearchModel,
    ProductUpdateModel,
)
from models.common_model import (
    ItemList,
    OutboundItemListResponse,
    OutboundResultantPagingModel,
)
from util.database import PagingModel
 

adapter: ProductDataAdapter = ProductDataAdapter()
common_adapter: CommonAdapters = CommonAdapters()
manager: ProductManager = ProductManager()


class ProductController:

    def create(
        self, inbound_model: ProductInboundCreateModel
    ) -> ProductOutboundModel | None:
        model: ProductCreateModel = (
            adapter.convert_from_inbound_create_model_to_create_model(
                inbound_model))

        result = manager.create(model)

        if result is None:
            raise Exception('Received no model from create operation.')

        response_model: ProductOutboundModel = (
            adapter.convert_from_model_to_outbound_model(result))

        return response_model

    def get_by_id(self, id: UUID) -> ProductOutboundModel | None:

        result = manager.get_by_id(id)

        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f'Product with id {id} not found.',
            )

        response_model: ProductOutboundModel = (
            adapter.convert_from_model_to_outbound_model(result))

        return response_model

    def search(
        self, inbound_model: ProductInboundSearchModel
    ) -> OutboundItemListResponse[ProductOutboundModel]:

        paging_model: PagingModel = (
            common_adapter.convert_from_paged_inbound_model_to_paging_model(
                inbound_model))

        search_model: ProductSearchModel = (
            adapter.convert_from_inbound_search_model_to_search_model(
                inbound_model))

        results: ItemList[ProductModel] = manager.search(
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
        inbound_model: ProductInboundUpdateModel,
        explicitNullSet: list[str] | None = None,
    ):

        explicitNullSet = explicitNullSet or []

        model: ProductUpdateModel = (
            adapter.convert_from_inbound_update_model_to_create_model(
                inbound_model))

        result: None | ProductModel = manager.update(id, model)

        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f'Product with id {id} not found.',
            )

        response_model: ProductOutboundModel = (
            adapter.convert_from_model_to_outbound_model(result))

        return response_model

    def delete(self, id: UUID):

        result = manager.delete(id)

        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f'Product with id {id} not found.',
            )

        response_model: ProductOutboundModel = (
            adapter.convert_from_model_to_outbound_model(result))

        return response_model
