from typing import Any
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
    CommonInboundPagedModel,
    OutboundResultantPagingModel,
)
from util.database import PagingModel, ResultantPagingModel


class CommonAdapters:

    def convert_from_paged_inbound_model_to_paging_model(
            self, inbound_model: CommonInboundPagedModel) -> PagingModel:

        model = PagingModel(
            page=inbound_model.page,
            page_length=inbound_model.page_length,
            sort_by=inbound_model.sort_by,
            is_sort_descending=inbound_model.is_sort_descending,
        )

        return model

    def convert_from_paging_model_to_outbound_paging_model(
            self, model: ResultantPagingModel) -> OutboundResultantPagingModel:

        outbound_model = OutboundResultantPagingModel(
            page=model.page,
            page_length=model.page_length,
            sort_by=model.sort_by,
            is_sort_descending=model.is_sort_descending,
            total_record_count=model.total_record_count,
        )

        return outbound_model
