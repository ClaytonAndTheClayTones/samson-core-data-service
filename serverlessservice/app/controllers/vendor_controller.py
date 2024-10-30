from uuid import UUID
from fastapi import HTTPException
from adapters.vendor_adapters import VendorDataAdapter
from adapters.common_adapters import CommonAdapters
from managers.vendor_manager import VendorManager
from models.vendor_model import (
    VendorCreateModel,
    VendorDatabaseModel,
    VendorInboundCreateModel,
    VendorInboundSearchModel,
    VendorInboundUpdateModel,
    VendorModel,
    VendorOutboundModel,
    VendorSearchModel,
    VendorUpdateModel,
)
from models.common_model import (
    ItemList,
    OutboundItemListResponse,
    OutboundResultantPagingModel,
)
from util.database import PagingModel
 
adapter: VendorDataAdapter = VendorDataAdapter()
common_adapter: CommonAdapters = CommonAdapters()
manager: VendorManager = VendorManager()


class VendorController:

    def create(
            self, inbound_model: VendorInboundCreateModel
    ) -> VendorOutboundModel | None:
        model: VendorCreateModel = (
            adapter.convert_from_inbound_create_model_to_create_model(
                inbound_model))

        result = manager.create(model)

        if result is None:
            raise Exception('Received no model from create operation.')

        response_model: VendorOutboundModel = (
            adapter.convert_from_model_to_outbound_model(result))

        return response_model

    def get_by_id(self, id: UUID) -> VendorOutboundModel | None:

        result = manager.get_by_id(id)

        if result is None:
            raise HTTPException(status_code=404,
                                detail=f'Vendor with id {id} not found.')

        response_model: VendorOutboundModel = (
            adapter.convert_from_model_to_outbound_model(result))

        return response_model

    def search(
        self, inbound_model: VendorInboundSearchModel
    ) -> OutboundItemListResponse[VendorOutboundModel]:

        paging_model: PagingModel = (
            common_adapter.convert_from_paged_inbound_model_to_paging_model(
                inbound_model))

        search_model: VendorSearchModel = (
            adapter.convert_from_inbound_search_model_to_search_model(
                inbound_model))

        results: ItemList[VendorModel] = manager.search(
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
        inbound_model: VendorInboundUpdateModel,
        explicitNullSet: list[str] | None = None,
    ):

        explicitNullSet = explicitNullSet or []

        model: VendorUpdateModel = (
            adapter.convert_from_inbound_update_model_to_create_model(
                inbound_model))

        result: None | VendorModel = manager.update(id, model)

        if result is None:
            raise HTTPException(status_code=404,
                                detail=f'Vendor with id {id} not found.')

        response_model: VendorOutboundModel = (
            adapter.convert_from_model_to_outbound_model(result))

        return response_model

    def delete(self, id: UUID):

        result = manager.delete(id)

        if result is None:
            raise HTTPException(status_code=404,
                                detail=f'Vendor with id {id} not found.')

        response_model: VendorOutboundModel = (
            adapter.convert_from_model_to_outbound_model(result))

        return response_model
