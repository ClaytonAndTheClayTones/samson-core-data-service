from fastapi import Depends, FastAPI, HTTPException, Response
from pydantic import UUID4
import uvicorn

from models.historical_sale_item_model import (
    HistoricalSaleItemInboundCreateModel,
    HistoricalSaleItemInboundSearchModel, 
    HistoricalSaleItemOutboundModel,
)
from controllers.historical_sale_item_controller import HistoricalSaleItemController
from models.common_model import (
    OutboundItemListResponse, )
from util.environment import Environment

controller: HistoricalSaleItemController = HistoricalSaleItemController()


def set_historical_sale_item_routes(app: FastAPI):

    @app.post(
        '/historical_sale_items',
        response_model=HistoricalSaleItemOutboundModel,
        status_code=201,
    )
    def post_retailerlocation(
        inbound_create_model: HistoricalSaleItemInboundCreateModel, ):
        result = controller.create(inbound_create_model)

        return result

    @app.get(
        '/historical_sale_items',
        response_model=OutboundItemListResponse[HistoricalSaleItemOutboundModel],
    )
    def get_retailer_locations(
        inbound_search_model: HistoricalSaleItemInboundSearchModel = Depends(),
    ) -> OutboundItemListResponse[HistoricalSaleItemOutboundModel]:

        result = controller.search(inbound_search_model)

        return result

    @app.get('/historical_sale_items/{id}',
             response_model=HistoricalSaleItemOutboundModel)
    def get_retailerlocation_by_id(id: UUID4):

        result = controller.get_by_id(id)

        return result
 
    @app.delete('/historical_sale_items/{id}',
                response_model=HistoricalSaleItemOutboundModel)
    def delete_retailerlocation(id: UUID4):

        result = controller.delete(id)

        return result
