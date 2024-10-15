from uuid import UUID
from data_accessors.pos_integration_accessor import PosIntegrationDataAccessor
from models.pos_integration_model import (
    PosIntegrationCreateModel,
    PosIntegrationModel,
    PosIntegrationSearchModel,
    PosIntegrationUpdateModel,
)
from models.common_model import ItemList
from util.database import PagingModel

accessor: PosIntegrationDataAccessor = PosIntegrationDataAccessor()


class PosIntegrationManager:

    def create(
            self, inboundModel: PosIntegrationCreateModel
    ) -> PosIntegrationModel | None:

        result = accessor.insert(inboundModel)

        return result

    def get_by_id(self, id: UUID):

        result = accessor.select_by_id(id)

        return result

    def search(
        self,
        model: PosIntegrationSearchModel,
        paging_model: PagingModel | None = None,
    ) -> ItemList[PosIntegrationModel]:

        result = accessor.select(model, paging_model)

        return result

    def update(
        self,
        id: UUID,
        model: PosIntegrationUpdateModel,
        explicit_null_set: list[str] | None = None,
    ):

        explicitNullSet = explicit_null_set or []

        result = accessor.update(id, model)

        return result

    def delete(self, id: UUID):

        result: None | PosIntegrationModel = accessor.delete(id)

        return result
