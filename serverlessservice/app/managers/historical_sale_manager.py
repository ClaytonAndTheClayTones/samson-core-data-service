from uuid import UUID
from data_accessors import vendor_accessor
from data_accessors.historical_sale_accessor import HistoricalSaleDataAccessor
from data_accessors.product_accessor import ProductDataAccessor
from data_accessors.retailer_location_accessor import RetailerLocationDataAccessor
from models.historical_sale_model import (
    HistoricalSaleCreateModel,
    HistoricalSaleModel,
    HistoricalSaleSearchModel, 
)
from models.common_model import ItemList
from util.database import PagingModel

accessor: HistoricalSaleDataAccessor = HistoricalSaleDataAccessor()
retailer_location_accessor: RetailerLocationDataAccessor = RetailerLocationDataAccessor()
product_accessor: ProductDataAccessor = ProductDataAccessor()


class HistoricalSaleManager:

    def create(
            self, 
            inboundModel: HistoricalSaleCreateModel
    ) -> HistoricalSaleModel | None:

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
        model: HistoricalSaleSearchModel,
        paging_model: PagingModel | None = None,
    ) -> ItemList[HistoricalSaleModel]:

        result = accessor.select(model, paging_model)

        return result
 

    def delete(self, id: UUID):

        result: None | HistoricalSaleModel = accessor.delete(id)

        return result
