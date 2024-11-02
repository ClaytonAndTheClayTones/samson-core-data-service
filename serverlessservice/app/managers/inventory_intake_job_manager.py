from uuid import UUID
from data_accessors.inventory_intake_job_accessor import InventoryIntakeJobDataAccessor
from data_accessors.retailer_location_accessor import RetailerLocationDataAccessor
from models.inventory_intake_job_model import (
    InventoryIntakeJobCreateModel,
    InventoryIntakeJobModel,
    InventoryIntakeJobSearchModel,
    InventoryIntakeJobUpdateModel,
)
from models.common_model import ItemList
from util.database import PagingModel

accessor: InventoryIntakeJobDataAccessor = InventoryIntakeJobDataAccessor()
retailer_location_accessor: RetailerLocationDataAccessor = RetailerLocationDataAccessor()


class InventoryIntakeJobManager:

    def create(
            self, 
            inboundModel: InventoryIntakeJobCreateModel
    ) -> InventoryIntakeJobModel | None:

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
        model: InventoryIntakeJobSearchModel,
        paging_model: PagingModel | None = None,
    ) -> ItemList[InventoryIntakeJobModel]:

        result = accessor.select(model, paging_model)

        return result

    def update(
        self,
        id: UUID,
        model: InventoryIntakeJobUpdateModel,
        explicit_null_set: list[str] | None = None,
    ):

        explicitNullSet = explicit_null_set or []

        result = accessor.update(id, model,explicitNullSet)

        return result

    def delete(self, id: UUID):

        result: None | InventoryIntakeJobModel = accessor.delete(id)

        return result
