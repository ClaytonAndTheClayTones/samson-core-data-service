from uuid import UUID
from data_accessors.retailer_location_accessor import (
    RetailerLocationDataAccessor, )
from models.retailer_location_model import (
    RetailerLocationCreateModel,
    RetailerLocationModel,
    RetailerLocationSearchModel,
    RetailerLocationUpdateModel,
)
from models.common_model import ItemList
from util.database import PagingModel

accessor: RetailerLocationDataAccessor = RetailerLocationDataAccessor()


class RetailerLocationManager:

    def create(
        self, inboundModel: RetailerLocationCreateModel
    ) -> RetailerLocationModel | None:

        result = accessor.insert(inboundModel)

        return result

    def get_by_id(self, id: UUID):

        result = accessor.select_by_id(id)

        return result

    def search(
        self,
        model: RetailerLocationSearchModel,
        paging_model: PagingModel | None = None,
    ) -> ItemList[RetailerLocationModel]:

        result = accessor.select(model, paging_model)

        return result

    def update(
        self,
        id: UUID,
        model: RetailerLocationUpdateModel,
        explicit_null_set: list[str] | None = None,
    ):

        explicitNullSet = explicit_null_set or []

        result = accessor.update(id, model)

        return result

    def delete(self, id: UUID):

        result: None | RetailerLocationModel = accessor.delete(id)

        return result
