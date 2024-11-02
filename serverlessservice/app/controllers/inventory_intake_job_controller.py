from copy import copy
from datetime import datetime
from uuid import UUID

from fastapi import HTTPException
from adapters.inventory_intake_job_adapters import InventoryIntakeJobDataAdapter
from adapters.common_adapters import CommonAdapters
from managers.inventory_intake_job_manager import InventoryIntakeJobManager
from models.inventory_intake_job_model import (
    InventoryIntakeJobCreateModel,
    InventoryIntakeJobDatabaseModel,
    InventoryIntakeJobInboundCreateModel,
    InventoryIntakeJobInboundSearchModel,
    InventoryIntakeJobInboundUpdateModel,
    InventoryIntakeJobModel,
    InventoryIntakeJobOutboundModel,
    InventoryIntakeJobSearchModel,
    InventoryIntakeJobUpdateModel,
)
from models.common_model import (
    ItemList,
    OutboundItemListResponse,
    OutboundResultantPagingModel,
)
from util.database import PagingModel
 
adapter: InventoryIntakeJobDataAdapter = InventoryIntakeJobDataAdapter()
common_adapter: CommonAdapters = CommonAdapters()
manager: InventoryIntakeJobManager = InventoryIntakeJobManager()


class InventoryIntakeJobController:

    def create(
        self, inbound_model: InventoryIntakeJobInboundCreateModel
    ) -> InventoryIntakeJobOutboundModel | None:
        model: InventoryIntakeJobCreateModel = (
            adapter.convert_from_inbound_create_model_to_create_model(
                inbound_model))

        result = manager.create(model)

        if result is None:
            raise Exception('Received no model from create operation.')

        response_model: InventoryIntakeJobOutboundModel = (
            adapter.convert_from_model_to_outbound_model(result))

        return response_model

    def get_by_id(self, id: UUID) -> InventoryIntakeJobOutboundModel | None:

        result = manager.get_by_id(id)

        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f'InventoryIntakeJob with id {id} not found.',
            )

        response_model: InventoryIntakeJobOutboundModel = (
            adapter.convert_from_model_to_outbound_model(result))

        return response_model

    def search(
        self, inbound_model: InventoryIntakeJobInboundSearchModel
    ) -> OutboundItemListResponse[InventoryIntakeJobOutboundModel]:

        paging_model: PagingModel = (
            common_adapter.convert_from_paged_inbound_model_to_paging_model(
                inbound_model))

        search_model: InventoryIntakeJobSearchModel = (
            adapter.convert_from_inbound_search_model_to_search_model(
                inbound_model))

        results: ItemList[InventoryIntakeJobModel] = manager.search(
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
        inbound_model: InventoryIntakeJobInboundUpdateModel,
        explicitNullSet: list[str] | None = None,
    ):

        explicitNullSet = explicitNullSet or []

        model: InventoryIntakeJobUpdateModel = (
            adapter.convert_from_inbound_update_model_to_create_model(
                inbound_model))

        result: None | InventoryIntakeJobModel = manager.update(id, model)

        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f'InventoryIntakeJob with id {id} not found.',
            )

        response_model: InventoryIntakeJobOutboundModel = (
            adapter.convert_from_model_to_outbound_model(result))

        return response_model

    def delete(self, id: UUID):

        result = manager.delete(id)

        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f'InventoryIntakeJob with id {id} not found.',
            )

        response_model: InventoryIntakeJobOutboundModel = (
            adapter.convert_from_model_to_outbound_model(result))

        return response_model
