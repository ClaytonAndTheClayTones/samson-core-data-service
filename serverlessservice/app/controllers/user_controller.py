from uuid import UUID
from fastapi import HTTPException
from adapters.user_adapters import UserDataAdapter
from adapters.common_adapters import CommonAdapters
from managers.user_manager import UserManager
from models.user_model import (
    UserCreateModel,
    UserDatabaseModel,
    UserInboundCreateModel,
    UserInboundSearchModel,
    UserInboundUpdateModel,
    UserModel,
    UserOutboundModel,
    UserSearchModel,
    UserUpdateModel,
)
from models.common_model import (
    ItemList,
    OutboundItemListResponse,
    OutboundResultantPagingModel,
)
from util.database import PagingModel 

adapter: UserDataAdapter = UserDataAdapter()
common_adapter: CommonAdapters = CommonAdapters()
manager: UserManager = UserManager()


class UserController:

    def create(
            self, inbound_model: UserInboundCreateModel
    ) -> UserOutboundModel | None:
        model: UserCreateModel = (
            adapter.convert_from_inbound_create_model_to_create_model(
                inbound_model))

        result = manager.create(model)

        if result is None:
            raise Exception('Received no model from create operation.')

        response_model: UserOutboundModel = (
            adapter.convert_from_model_to_outbound_model(result))

        return response_model

    def get_by_id(self, id: UUID) -> UserOutboundModel | None:

        result = manager.get_by_id(id)

        if result is None:
            raise HTTPException(status_code=404,
                                detail=f'User with id {id} not found.')

        response_model: UserOutboundModel = (
            adapter.convert_from_model_to_outbound_model(result))

        return response_model

    def search(
        self, inbound_model: UserInboundSearchModel
    ) -> OutboundItemListResponse[UserOutboundModel]:

        paging_model: PagingModel = (
            common_adapter.convert_from_paged_inbound_model_to_paging_model(
                inbound_model))

        search_model: UserSearchModel = (
            adapter.convert_from_inbound_search_model_to_search_model(
                inbound_model))

        results: ItemList[UserModel] = manager.search(
            search_model, paging_model)

        return_result_list = list(
            map(
                lambda x: adapter.convert_from_model_to_outbound_model(x),
                results.items,
            ))

        outbound_paging: OutboundResultantPagingModel = (
            common_adapter.convert_from_paging_model_to_outbound_paging_model(
                results.paging))

        return_result = OutboundItemListResponse(items=return_result_list,
                                                 paging=outbound_paging)

        return return_result

    def update(
        self,
        id: UUID,
        inbound_model: UserInboundUpdateModel,
        explicitNullSet: list[str] | None = None,
    ):

        explicitNullSet = explicitNullSet or []

        model: UserUpdateModel = (
            adapter.convert_from_inbound_update_model_to_create_model(
                inbound_model))

        result: None | UserModel = manager.update(id, model)

        if result is None:
            raise HTTPException(status_code=404,
                                detail=f'User with id {id} not found.')

        response_model: UserOutboundModel = (
            adapter.convert_from_model_to_outbound_model(result))

        return response_model

    def delete(self, id: UUID):

        result = manager.delete(id)

        if result is None:
            raise HTTPException(status_code=404,
                                detail=f'User with id {id} not found.')

        response_model: UserOutboundModel = (
            adapter.convert_from_model_to_outbound_model(result))

        return response_model
