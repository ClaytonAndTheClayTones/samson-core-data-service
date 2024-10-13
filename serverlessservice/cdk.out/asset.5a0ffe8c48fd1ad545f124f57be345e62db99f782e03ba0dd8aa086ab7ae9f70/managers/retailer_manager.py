from uuid import UUID
from data_accessors.retailer_accessor import RetailerDataAccessor
from models.retailer_model import (
    RetailerCreateModel,
    RetailerModel,
    RetailerSearchModel,
    RetailerUpdateModel,
)
from models.common_model import ItemList
from util.database import PagingModel

accessor: RetailerDataAccessor = RetailerDataAccessor()


class RetailerManager:

    def create(self,
               inboundModel: RetailerCreateModel) -> RetailerModel | None:

        result = accessor.insert(inboundModel)

        return result

    def get_by_id(self, id: UUID):

        result = accessor.select_by_id(id)

        return result

    def search(
        self,
        model: RetailerSearchModel,
        paging_model: PagingModel | None = None,
    ) -> ItemList[RetailerModel]:

        result = accessor.select(model, paging_model)

        return result

    def update(
        self,
        id: UUID,
        model: RetailerUpdateModel,
        explicit_null_set: list[str] | None = None,
    ):

        explicitNullSet = explicit_null_set or []

        result = accessor.update(id, model, explicitNullSet)

        return result

    def delete(self, id: UUID):

        result: None | RetailerModel = accessor.delete(id)

        return result
