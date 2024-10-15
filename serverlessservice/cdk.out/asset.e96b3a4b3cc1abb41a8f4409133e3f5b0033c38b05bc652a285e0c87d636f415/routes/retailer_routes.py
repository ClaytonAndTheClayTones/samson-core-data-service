
from fastapi import Depends, FastAPI
from pydantic import UUID4

from models.retailer_model import (
    RetailerInboundCreateModel,
    RetailerInboundSearchModel,
    RetailerInboundUpdateModel,
    RetailerOutboundModel,
)
from controllers.retailer_controller import RetailerController
from models.common_model import ( 
    OutboundItemListResponse,
)
from util.environment import Environment

controller: RetailerController = RetailerController()


def set_retailer_routes(app: FastAPI):

    @app.post('/retailers',
              response_model=RetailerOutboundModel,
              status_code=201)
    def post_retailer(inbound_create_model: RetailerInboundCreateModel):
        result = controller.create(inbound_create_model)

        return result

    @app.get(
        '/retailers',
        response_model=OutboundItemListResponse[RetailerOutboundModel],
    )
    def get_retailers(
        inbound_search_model: RetailerInboundSearchModel = Depends(),
    ) -> OutboundItemListResponse[RetailerOutboundModel]:

        result = controller.search(inbound_search_model)

        return result

    @app.get('/retailers/{id}', response_model=RetailerOutboundModel)
    def get_retailer_by_id(id: UUID4):

        result = controller.get_by_id(id)

        return result

    @app.patch('/retailers/{id}', response_model=RetailerOutboundModel)
    def patch_retailer(id: UUID4,
                       inbound_update_model: RetailerInboundUpdateModel):
        result = controller.update(id, inbound_update_model)

        return result

    @app.delete('/retailers/{id}', response_model=RetailerOutboundModel)
    def delete_retailer(id: UUID4):

        result = controller.delete(id)

        return result
