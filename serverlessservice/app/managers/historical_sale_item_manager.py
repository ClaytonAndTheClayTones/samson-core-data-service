from uuid import UUID
from data_accessors import vendor_accessor
from data_accessors.historical_sale_accessor import HistoricalSaleDataAccessor
from data_accessors.historical_sale_item_accessor import HistoricalSaleItemDataAccessor
from data_accessors.product_accessor import ProductDataAccessor
from data_accessors.retailer_location_accessor import RetailerLocationDataAccessor
from data_accessors.sales_intake_job_accessor import SalesIntakeJobDataAccessor
from models.historical_sale_item_model import (
    HistoricalSaleItemCreateModel,
    HistoricalSaleItemModel,
    HistoricalSaleItemSearchModel, 
)
from models.common_model import ItemList
from util.database import PagingModel

accessor: HistoricalSaleItemDataAccessor = HistoricalSaleItemDataAccessor()
retailer_location_accessor: RetailerLocationDataAccessor = RetailerLocationDataAccessor()
sales_intake_job_accessor: SalesIntakeJobDataAccessor = SalesIntakeJobDataAccessor()
product_accessor: ProductDataAccessor = ProductDataAccessor()
historical_sales_accessor: HistoricalSaleDataAccessor = HistoricalSaleDataAccessor()


class HistoricalSaleItemManager:

    def create(
            self, 
            inboundModel: HistoricalSaleItemCreateModel
    ) -> HistoricalSaleItemModel | None:
 
        # Denormalize product_vendor_id
        
        referenced_product = product_accessor.select_by_id(inboundModel.product_id)
        
        inboundModel.product_vendor_id = referenced_product.vendor_id
        
        # Denormalize intake_job_id, retailer_location_id, and retailer_id

        referenced_historical_sale = historical_sales_accessor.select_by_id(inboundModel.historical_sale_id)
        
        inboundModel.retailer_id = referenced_historical_sale.retailer_id
        inboundModel.retailer_location_id = referenced_historical_sale.retailer_location_id
        inboundModel.sales_intake_job_id = referenced_historical_sale.sales_intake_job_id
        
        result = accessor.insert(inboundModel)
        
        return result

    def get_by_id(self, id: UUID):

        result = accessor.select_by_id(id)

        return result

    def search(
        self,
        model: HistoricalSaleItemSearchModel,
        paging_model: PagingModel | None = None,
    ) -> ItemList[HistoricalSaleItemModel]:

        result = accessor.select(model, paging_model)

        return result
 

    def delete(self, id: UUID):

        result: None | HistoricalSaleItemModel = accessor.delete(id)

        return result
