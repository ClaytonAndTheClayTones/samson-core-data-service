from uuid import UUID
from data_accessors.pos_integration_accessor import PosIntegrationDataAccessor
from data_accessors.pos_integration_call_accessor import PosIntegrationCallDataAccessor
from data_accessors.retailer_location_accessor import RetailerLocationDataAccessor
from models.pos_integration_call_model import (
    PosIntegrationCallCreateModel,
    PosIntegrationCallModel,
    PosIntegrationCallSearchModel, 
)
from models.common_model import ItemList
from util.database import PagingModel

accessor: PosIntegrationCallDataAccessor = PosIntegrationCallDataAccessor()
pos_integration_accessor: PosIntegrationDataAccessor = PosIntegrationDataAccessor()


class PosIntegrationCallManager:

    def create(
            self, 
            inboundModel: PosIntegrationCallCreateModel
    ) -> PosIntegrationCallModel | None:

        # Denormalize retailer_id
        
        pos_integration = pos_integration_accessor.select_by_id(inboundModel.pos_integration_id)
        
        inboundModel.retailer_id = pos_integration.retailer_id
        inboundModel.retailer_location_id = pos_integration.retailer_location_id

        result = accessor.insert(inboundModel)

        return result

    def get_by_id(self, id: UUID):

        result = accessor.select_by_id(id)

        return result

    def search(
        self,
        model: PosIntegrationCallSearchModel,
        paging_model: PagingModel | None = None,
    ) -> ItemList[PosIntegrationCallModel]:

        result = accessor.select(model, paging_model)

        return result

    def delete(self, id: UUID):

        result: None | PosIntegrationCallModel = accessor.delete(id)

        return result
