from fastapi import Depends, FastAPI 
from pydantic import UUID4 

from models.pos_integration_model import (
    PosIntegrationInboundCreateModel,
    PosIntegrationInboundSearchModel,
    PosIntegrationInboundUpdateModel,
    PosIntegrationOutboundModel,
)
from controllers.pos_integration_controller import PosIntegrationController
from models.common_model import (
    OutboundItemListResponse
)
 

controller: PosIntegrationController = PosIntegrationController()


def set_pos_integration_routes(app: FastAPI):

    @app.post(
        '/pos_integrations',
        response_model=PosIntegrationOutboundModel,
        status_code=201,
    )
    def post_retailerlocation(
        inbound_create_model: PosIntegrationInboundCreateModel, ):
        result = controller.create(inbound_create_model)

        return result

    @app.get(
        '/pos_integrations',
        response_model=OutboundItemListResponse[PosIntegrationOutboundModel],
    )
    def get_retailer_locations(
        inbound_search_model: PosIntegrationInboundSearchModel = Depends(),
    ) -> OutboundItemListResponse[PosIntegrationOutboundModel]:

        result = controller.search(inbound_search_model)

        return result

    @app.get('/pos_integrations/{id}',
             response_model=PosIntegrationOutboundModel)
    def get_retailerlocation_by_id(id: UUID4):

        result = controller.get_by_id(id)

        return result

    @app.patch('/pos_integrations/{id}',
               response_model=PosIntegrationOutboundModel)
    def patch_retailerlocation(
            id: UUID4, inbound_update_model: PosIntegrationInboundUpdateModel):
        result = controller.update(id, inbound_update_model)

        return result

    @app.delete('/pos_integrations/{id}',
                response_model=PosIntegrationOutboundModel)
    def delete_retailerlocation(id: UUID4):

        result = controller.delete(id)

        return result
