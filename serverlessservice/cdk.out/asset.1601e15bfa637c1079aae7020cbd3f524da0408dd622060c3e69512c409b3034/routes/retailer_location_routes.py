from fastapi import Depends, FastAPI, HTTPException, Response
from pydantic import UUID4
import uvicorn

from models.retailer_location_model import (
    RetailerLocationInboundCreateModel,
    RetailerLocationInboundSearchModel,
    RetailerLocationInboundUpdateModel,
    RetailerLocationOutboundModel,
)
from controllers.retailer_location_controller import RetailerLocationController
from models.common_model import (
    CommonOutboundResponseModel,
    OutboundItemListResponse,
)
from util.environment import Environment

controller: RetailerLocationController = RetailerLocationController()


def set_retailer_location_routes(app: FastAPI):

    @app.post(
        '/retailer_locations',
        response_model=RetailerLocationOutboundModel,
        status_code=201,
    )
    def post_retailerlocation(
        inbound_create_model: RetailerLocationInboundCreateModel, ):
        result = controller.create(inbound_create_model)

        return result

    @app.get(
        '/retailer_locations',
        response_model=OutboundItemListResponse[RetailerLocationOutboundModel],
    )
    def get_retailer_locations(
        inbound_search_model: RetailerLocationInboundSearchModel = Depends(),
    ) -> OutboundItemListResponse[RetailerLocationOutboundModel]:

        result = controller.search(inbound_search_model)

        return result

    @app.get(
        '/retailer_locations/{id}',
        response_model=RetailerLocationOutboundModel,
    )
    def get_retailerlocation_by_id(id: UUID4):

        result = controller.get_by_id(id)

        return result

    @app.patch(
        '/retailer_locations/{id}',
        response_model=RetailerLocationOutboundModel,
    )
    def patch_retailerlocation(
            id: UUID4,
            inbound_update_model: RetailerLocationInboundUpdateModel):
        result = controller.update(id, inbound_update_model)

        return result

    @app.delete(
        '/retailer_locations/{id}',
        response_model=RetailerLocationOutboundModel,
    )
    def delete_retailerlocation(id: UUID4):

        result = controller.delete(id)

        return result
