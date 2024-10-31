from uuid import UUID
from data_accessors.product_accessor import (
    ProductDataAccessor, )
from data_accessors.retailer_location_accessor import RetailerLocationDataAccessor
from models.product_model import (
    ProductCreateModel,
    ProductModel,
    ProductSearchModel,
    ProductUpdateModel,
)
from models.common_model import ItemList
from util.database import PagingModel

accessor: ProductDataAccessor = ProductDataAccessor()
retail_location_accessor: RetailerLocationDataAccessor = RetailerLocationDataAccessor()

class ProductManager:

    def create(
        self, inboundModel: ProductCreateModel
    ) -> ProductModel | None:
        
        # Denormalize retailer_id
        
        if(inboundModel.referring_retailer_location_id):
            referenced_retailer_location = retail_location_accessor.select_by_id(inboundModel.referring_retailer_location_id)
            inboundModel.referring_retailer_id = referenced_retailer_location.retailer_id

        result = accessor.insert(inboundModel)

        return result

    def get_by_id(self, id: UUID):

        result = accessor.select_by_id(id)

        return result

    def search(
        self,
        model: ProductSearchModel,
        paging_model: PagingModel | None = None,
    ) -> ItemList[ProductModel]:
    
        result = accessor.select(model, paging_model)

        return result

    def update(
        self,
        id: UUID,
        model: ProductUpdateModel,
        explicit_null_set: list[str] | None = None,
    ):   
        explicitNullSet = explicit_null_set or []

        result = accessor.update(id, model, explicitNullSet)

        return result

    def delete(self, id: UUID):

        result: None | ProductModel = accessor.delete(id)

        return result
