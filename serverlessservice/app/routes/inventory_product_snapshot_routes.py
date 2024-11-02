from fastapi import Depends, FastAPI, HTTPException, Response
from pydantic import UUID4
import uvicorn

from models.inventory_product_snapshot_model import (
    InventoryProductSnapshotInboundCreateModel,
    InventoryProductSnapshotInboundSearchModel, 
    InventoryProductSnapshotOutboundModel,
)
from controllers.inventory_product_snapshot_controller import InventoryProductSnapshotController
from models.common_model import (
    OutboundItemListResponse, )
from util.environment import Environment

controller: InventoryProductSnapshotController = InventoryProductSnapshotController()


def set_inventory_product_snapshot_routes(app: FastAPI):

    @app.post(
        '/inventory_product_snapshots',
        response_model=InventoryProductSnapshotOutboundModel,
        status_code=201,
    )
    def post_retailerlocation(
        inbound_create_model: InventoryProductSnapshotInboundCreateModel, ):
        result = controller.create(inbound_create_model)

        return result

    @app.get(
        '/inventory_product_snapshots',
        response_model=OutboundItemListResponse[InventoryProductSnapshotOutboundModel],
    )
    def get_retailer_locations(
        inbound_search_model: InventoryProductSnapshotInboundSearchModel = Depends(),
    ) -> OutboundItemListResponse[InventoryProductSnapshotOutboundModel]:

        result = controller.search(inbound_search_model)

        return result

    @app.get('/inventory_product_snapshots/{id}',
             response_model=InventoryProductSnapshotOutboundModel)
    def get_retailerlocation_by_id(id: UUID4):

        result = controller.get_by_id(id)

        return result
 
    @app.delete('/inventory_product_snapshots/{id}',
                response_model=InventoryProductSnapshotOutboundModel)
    def delete_retailerlocation(id: UUID4):

        result = controller.delete(id)

        return result
