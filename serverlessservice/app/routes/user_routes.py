from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Response
from pydantic import UUID4, Strict
import uvicorn

from models.user_model import (
    UserInboundCreateModel,
    UserInboundSearchModel,
    UserInboundUpdateModel,
    UserOutboundModel,
)
from controllers.user_controller import UserController
from models.common_model import (
    CommonOutboundResponseModel,
    OutboundItemListResponse,
)
from util.environment import Environment

controller: UserController = UserController()


def set_user_routes(app: FastAPI):

    @app.post('/users', response_model=UserOutboundModel, status_code=201)
    def post_user(inbound_create_model: UserInboundCreateModel):
        result = controller.create(inbound_create_model)

        return result

    @app.get(
        '/users',
        response_model=OutboundItemListResponse[UserOutboundModel],
    )
    def get_users(
        inbound_search_model: UserInboundSearchModel = Depends(),
    ) -> OutboundItemListResponse[UserOutboundModel]:

        result = controller.search(inbound_search_model)

        return result

    @app.get('/users/{id}', response_model=UserOutboundModel)
    def get_user_by_id(id: UUID4):

        result = controller.get_by_id(id)

        return result

    @app.patch('/users/{id}', response_model=UserOutboundModel)
    def patch_user(id: UUID4,
                     inbound_update_model: UserInboundUpdateModel):
        result = controller.update(id, inbound_update_model)

        return result

    @app.delete('/users/{id}', response_model=UserOutboundModel)
    def delete_user(id: UUID4):

        result = controller.delete(id)

        return result
