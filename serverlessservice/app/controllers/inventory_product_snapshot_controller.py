from copy import copy
from datetime import datetime
from uuid import UUID

from fastapi import HTTPException
from adapters.inventory_product_snapshot_adapters import InventoryProductSnapshotDataAdapter
from adapters.common_adapters import CommonAdapters
from managers.inventory_product_snapshot_manager import InventoryProductSnapshotManager
from models.inventory_product_snapshot_model import (
    InventoryProductSnapshotCreateModel,
    InventoryProductSnapshotDatabaseModel,
    InventoryProductSnapshotInboundCreateModel,
    InventoryProductSnapshotInboundSearchModel, 
    InventoryProductSnapshotModel,
    InventoryProductSnapshotOutboundModel,
    InventoryProductSnapshotSearchModel, 
)
from models.common_model import (
    ItemList,
    OutboundItemListResponse,
    OutboundResultantPagingModel,
)
from util.database import PagingModel
 
adapter: InventoryProductSnapshotDataAdapter = InventoryProductSnapshotDataAdapter()
common_adapter: CommonAdapters = CommonAdapters()
manager: InventoryProductSnapshotManager = InventoryProductSnapshotManager()


class InventoryProductSnapshotController:

    def create(
        self, inbound_model: InventoryProductSnapshotInboundCreateModel
    ) -> InventoryProductSnapshotOutboundModel | None:
        model: InventoryProductSnapshotCreateModel = (
            adapter.convert_from_inbound_create_model_to_create_model(
                inbound_model))

        result = manager.create(model)

        if result is None:
            raise Exception('Received no model from create operation.')

        response_model: InventoryProductSnapshotOutboundModel = (
            adapter.convert_from_model_to_outbound_model(result))

        return response_model

    def get_by_id(self, id: UUID) -> InventoryProductSnapshotOutboundModel | None:

        result = manager.get_by_id(id)

        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f'InventoryProductSnapshot with id {id} not found.',
            )

        response_model: InventoryProductSnapshotOutboundModel = (
            adapter.convert_from_model_to_outbound_model(result))

        return response_model

    def search(
        self, inbound_model: InventoryProductSnapshotInboundSearchModel
    ) -> OutboundItemListResponse[InventoryProductSnapshotOutboundModel]:

        paging_model: PagingModel = (
            common_adapter.convert_from_paged_inbound_model_to_paging_model(
                inbound_model))

        search_model: InventoryProductSnapshotSearchModel = (
            adapter.convert_from_inbound_search_model_to_search_model(
                inbound_model))

        results: ItemList[InventoryProductSnapshotModel] = manager.search(
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
                detail=f'InventoryProductSnapshot with id {id} not found.',
            )

        response_model: InventoryProductSnapshotOutboundModel = (
            adapter.convert_from_model_to_outbound_model(result))

        return response_model
