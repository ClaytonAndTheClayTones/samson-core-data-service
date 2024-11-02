from uuid import UUID
from data_accessors.inventory_product_snapshot_accessor import InventoryProductSnapshotDataAccessor
from data_accessors.retailer_location_accessor import RetailerLocationDataAccessor
from models.inventory_product_snapshot_model import (
    InventoryProductSnapshotCreateModel,
    InventoryProductSnapshotModel,
    InventoryProductSnapshotSearchModel, 
)
from models.common_model import ItemList
from util.database import PagingModel

accessor: InventoryProductSnapshotDataAccessor = InventoryProductSnapshotDataAccessor()
retailer_location_accessor: RetailerLocationDataAccessor = RetailerLocationDataAccessor()


class InventoryProductSnapshotManager:

    def create(
            self, 
            inboundModel: InventoryProductSnapshotCreateModel
    ) -> InventoryProductSnapshotModel | None:

        # Denormalize retailer_id
        
        referenced_retailer_location = retailer_location_accessor.select_by_id(inboundModel.retailer_location_id)
        
        inboundModel.retailer_id = referenced_retailer_location.retailer_id

        result = accessor.insert(inboundModel)

        return result

    def get_by_id(self, id: UUID):

        result = accessor.select_by_id(id)

        return result

    def search(
        self,
        model: InventoryProductSnapshotSearchModel,
        paging_model: PagingModel | None = None,
    ) -> ItemList[InventoryProductSnapshotModel]:

        result = accessor.select(model, paging_model)

        return result
 

    def delete(self, id: UUID):

        result: None | InventoryProductSnapshotModel = accessor.delete(id)

        return result
