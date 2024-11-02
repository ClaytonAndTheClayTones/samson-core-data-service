from fastapi import Depends, FastAPI, HTTPException, Response
from pydantic import UUID4
import uvicorn

from models.inventory_intake_job_model import (
    InventoryIntakeJobInboundCreateModel,
    InventoryIntakeJobInboundSearchModel,
    InventoryIntakeJobInboundUpdateModel,
    InventoryIntakeJobOutboundModel,
)
from controllers.inventory_intake_job_controller import InventoryIntakeJobController
from models.common_model import (
    OutboundItemListResponse, )
from util.environment import Environment

controller: InventoryIntakeJobController = InventoryIntakeJobController()


def set_inventory_intake_job_routes(app: FastAPI):

    @app.post(
        '/inventory_intake_jobs',
        response_model=InventoryIntakeJobOutboundModel,
        status_code=201,
    )
    def post_retailerlocation(
        inbound_create_model: InventoryIntakeJobInboundCreateModel, ):
        result = controller.create(inbound_create_model)

        return result

    @app.get(
        '/inventory_intake_jobs',
        response_model=OutboundItemListResponse[InventoryIntakeJobOutboundModel],
    )
    def get_retailer_locations(
        inbound_search_model: InventoryIntakeJobInboundSearchModel = Depends(),
    ) -> OutboundItemListResponse[InventoryIntakeJobOutboundModel]:

        result = controller.search(inbound_search_model)

        return result

    @app.get('/inventory_intake_jobs/{id}',
             response_model=InventoryIntakeJobOutboundModel)
    def get_retailerlocation_by_id(id: UUID4):

        result = controller.get_by_id(id)

        return result

    @app.patch('/inventory_intake_jobs/{id}',
               response_model=InventoryIntakeJobOutboundModel)
    def patch_retailerlocation(
            id: UUID4, inbound_update_model: InventoryIntakeJobInboundUpdateModel):
        result = controller.update(id, inbound_update_model)

        return result

    @app.delete('/inventory_intake_jobs/{id}',
                response_model=InventoryIntakeJobOutboundModel)
    def delete_retailerlocation(id: UUID4):

        result = controller.delete(id)

        return result
