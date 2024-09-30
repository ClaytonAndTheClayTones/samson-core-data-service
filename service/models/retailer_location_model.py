from datetime import datetime
from enum import Enum
from typing import Annotated, Optional
from uuid import UUID
from fastapi import Query
from pydantic import UUID4, BaseModel, BeforeValidator, EmailStr, Field, Strict

from models.common_model import (
    CommonDatabaseModel,
    CommonInboundSearchModel,
    CommonModel,
    CommonOutboundResponseModel,
    CommonSearchModel,
    DicsPhoneNumber,
    validate_ids,
)


# Pydantic causes these class variables to safely be instance variables.
class RetailerLocationInboundCreateModel(BaseModel):
    name: str = Field(..., max_length=255)
    retailer_id: Annotated[UUID4, Strict(False)]
    pos_integration_id: Optional[Annotated[UUID4, Strict(False)]] = Field(
        default=None
    )
    contact_email: Optional[EmailStr] = Field(default=None, max_length=320)
    contact_phone: Optional[DicsPhoneNumber] = Field(
        default=None, max_length=32
    )
    location_city: Optional[str] = Field(default=None, max_length=255)
    location_state: Optional[str] = Field(default=None, max_length=255)
    location_country: Optional[str] = Field(
        default=None, max_length=2, min_length=2
    )


# Pydantic causes these class variables to safely be instance variables.
class RetailerLocationInboundUpdateModel(BaseModel):
    name: Optional[str] = Field(default=None, max_length=255)
    pos_integration_id: Optional[Annotated[UUID4, Strict(False)]] = Field(
        default=None
    )
    contact_email: Optional[EmailStr] = Field(default=None, max_length=320)
    contact_phone: Optional[DicsPhoneNumber] = Field(
        default=None, max_length=32
    )
    location_city: Optional[str] = Field(default=None, max_length=255)
    location_state: Optional[str] = Field(default=None, max_length=255)
    location_country: Optional[str] = Field(
        default=None, max_length=2, min_length=2
    )


# Pydantic causes these class variables to safely be instance variables.
class RetailerLocationInboundSearchModel(CommonInboundSearchModel):
    name: Optional[str] = Query(default=None)
    name_like: Optional[str] = Query(default=None)
    retailer_ids: Annotated[
        Optional[str], BeforeValidator(validate_ids)
    ] = Query(default=None)
    pos_integration_ids: Annotated[
        Optional[str], BeforeValidator(validate_ids)
    ] = Query(default=None)
    location_city: Optional[str] = Query(default=None)
    location_state: Optional[str] = Query(default=None)
    location_country: Optional[str] = Query(default=None)


class RetailerLocationCreateModel:
    def __init__(
        self,
        name: str,
        retailer_id: UUID,
        contact_email: EmailStr | None = None,
        contact_phone: DicsPhoneNumber | None = None,
        pos_integration_id: str | None = None,
        location_city: str | None = None,
        location_state: str | None = None,
        location_country: str | None = None,
    ) -> None:

        self.name = name
        self.retailer_id = retailer_id
        self.pos_integration_id = pos_integration_id
        self.contact_email = contact_email
        self.contact_phone = contact_phone
        self.location_city = location_city
        self.location_state = location_state
        self.location_country = location_country


class RetailerLocationUpdateModel:
    def __init__(
        self,
        name: str | None = None,
        pos_integration_id: UUID | None = None,
        contact_email: EmailStr | None = None,
        contact_phone: DicsPhoneNumber | None = None,
        location_city: str | None = None,
        location_state: str | None = None,
        location_country: str | None = None,
    ) -> None:

        self.name = name
        self.pos_integration_id = pos_integration_id
        self.contact_email = contact_email
        self.contact_phone = contact_phone
        self.location_city = location_city
        self.location_state = location_state
        self.location_country = location_country


class RetailerLocationSearchModel(CommonSearchModel):
    def __init__(
        self,
        ids: list[UUID] | None = None,
        retailer_ids: list[UUID] | None = None,
        pos_integration_ids: list[UUID] | None = None,
        name: str | None = None,
        name_like: str | None = None,
        location_city: str | None = None,
        location_state: str | None = None,
        location_country: str | None = None,
    ) -> None:

        super().__init__(ids)

        self.name = name
        self.name_like = name_like
        self.retailer_ids = retailer_ids
        self.pos_integration_ids = pos_integration_ids
        self.location_city = location_city
        self.location_state = location_state
        self.location_country = location_country


class RetailerLocationDatabaseModel(CommonDatabaseModel):
    def __init__(
        self,
        id: UUID,
        retailer_id: UUID,
        name: str,
        created_at: datetime,
        pos_integration_id: UUID | None = None,
        location_city: str | None = None,
        location_state: str | None = None,
        location_country: str | None = None,
        contact_email: EmailStr | None = None,
        contact_phone: DicsPhoneNumber | None = None,
        updated_at: datetime | None = None,
    ):

        super().__init__(id, created_at, updated_at)

        self.name = name
        self.retailer_id = retailer_id
        self.pos_integration_id = pos_integration_id
        self.contact_email = contact_email
        self.contact_phone = contact_phone
        self.location_city = location_city
        self.location_state = location_state
        self.location_country = location_country


class RetailerLocationModel(CommonModel):
    def __init__(
        self,
        id: UUID,
        retailer_id: UUID,
        name: str,
        created_at: datetime,
        pos_integration_id: UUID | None = None,
        location_city: str | None = None,
        location_state: str | None = None,
        location_country: str | None = None,
        contact_email: EmailStr | None = None,
        contact_phone: DicsPhoneNumber | None = None,
        updated_at: datetime | None = None,
    ):

        super().__init__(id, created_at, updated_at)

        self.name = name
        self.retailer_id = retailer_id
        self.pos_integration_id = pos_integration_id
        self.contact_email = contact_email
        self.contact_phone = contact_phone
        self.location_city = location_city
        self.location_state = location_state
        self.location_country = location_country


# Pydantic causes these class variables to safely be instance variables.
class RetailerLocationOutboundModel(CommonOutboundResponseModel):
    name: str
    retailer_id: UUID
    pos_integration_id: UUID | None = None
    location_city: str | None = None
    location_state: str | None = None
    location_country: str | None = None
    contact_email: str | EmailStr = None
    contact_phone: str | DicsPhoneNumber = None
