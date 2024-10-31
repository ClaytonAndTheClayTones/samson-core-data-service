from uuid import UUID
from data_accessors.vendor_accessor import VendorDataAccessor
from models.vendor_model import (
    VendorCreateModel,
    VendorModel,
    VendorSearchModel,
    VendorUpdateModel,
)
from models.common_model import ItemList
from util.database import PagingModel

accessor: VendorDataAccessor = VendorDataAccessor()

class VendorManager:

    def create(self, inboundModel: VendorCreateModel) -> VendorModel | None:

        result = accessor.insert(inboundModel)

        return result

    def get_by_id(self, id: UUID):

        result = accessor.select_by_id(id)

        return result

    def search(
            self,
            model: VendorSearchModel,
            paging_model: PagingModel | None = None) -> ItemList[VendorModel]:

        result = accessor.select(model, paging_model)

        return result

    def update(
        self,
        id: UUID,
        model: VendorUpdateModel,
        explicit_null_set: list[str] | None = None,
    ):

        explicitNullSet = explicit_null_set or []

        result = accessor.update(id, model, explicitNullSet)

        return result

    def delete(self, id: UUID):

        result: None | VendorModel = accessor.delete(id)

        return result
