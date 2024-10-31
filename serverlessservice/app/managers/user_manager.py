from uuid import UUID
from data_accessors.retailer_location_accessor import RetailerLocationDataAccessor
from data_accessors.user_accessor import UserDataAccessor
from models.user_model import (
    UserCreateModel,
    UserModel,
    UserSearchModel,
    UserUpdateModel,
)
from models.common_model import ItemList
from util.database import PagingModel

accessor: UserDataAccessor = UserDataAccessor()
retailer_location_accessor: RetailerLocationDataAccessor = RetailerLocationDataAccessor()


class UserManager:

    def create(self, inboundModel: UserCreateModel) -> UserModel | None:

        # Denormalize retailer_id
        if(inboundModel.retailer_location_id): 
            referenced_retailer_location = retailer_location_accessor.select_by_id(inboundModel.retailer_location_id) 
            inboundModel.retailer_id = referenced_retailer_location.retailer_id
        
        result = accessor.insert(inboundModel)

        return result

    def get_by_id(self, id: UUID):

        result = accessor.select_by_id(id)

        return result

    def search(
            self,
            model: UserSearchModel,
            paging_model: PagingModel | None = None) -> ItemList[UserModel]:

        result = accessor.select(model, paging_model)

        return result

    def update(
        self,
        id: UUID,
        model: UserUpdateModel,
        explicit_null_set: list[str] | None = None,
    ):

        explicitNullSet = explicit_null_set or []

        result = accessor.update(id, model, explicitNullSet)

        return result

    def delete(self, id: UUID):

        result: None | UserModel = accessor.delete(id)

        return result
