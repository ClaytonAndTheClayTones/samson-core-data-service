from fastapi import Depends, FastAPI, HTTPException, Response
from pydantic import UUID4
import uvicorn

from models.pos_integration_call_model import (
    PosIntegrationCallInboundCreateModel,
    PosIntegrationCallInboundSearchModel, 
    PosIntegrationCallOutboundModel,
)
from controllers.pos_integration_call_controller import PosIntegrationCallController
from models.common_model import (
    OutboundItemListResponse, )
from util.environment import Environment

controller: PosIntegrationCallController = PosIntegrationCallController()


def set_pos_integration_call_routes(app: FastAPI):

    @app.post(
        '/pos_integration_calls',
        response_model=PosIntegrationCallOutboundModel,
        status_code=201,
    )
    def post_retailerlocation(
        inbound_create_model: PosIntegrationCallInboundCreateModel, ):
        result = controller.create(inbound_create_model)

        return result

    @app.get(
        '/pos_integration_calls',
        response_model=OutboundItemListResponse[PosIntegrationCallOutboundModel],
    )
    def get_retailer_locations(
        inbound_search_model: PosIntegrationCallInboundSearchModel = Depends(),
    ) -> OutboundItemListResponse[PosIntegrationCallOutboundModel]:

        result = controller.search(inbound_search_model)

        return result

    @app.get('/pos_integration_calls/{id}',
             response_model=PosIntegrationCallOutboundModel)
    def get_retailerlocation_by_id(id: UUID4):

        result = controller.get_by_id(id)

        return result
  
    @app.delete('/pos_integration_calls/{id}',
                response_model=PosIntegrationCallOutboundModel)
    def delete_retailerlocation(id: UUID4):

        result = controller.delete(id)

        return result
