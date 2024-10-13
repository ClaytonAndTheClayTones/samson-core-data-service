from datetime import datetime
from enum import Enum
from typing import Annotated, Optional
from uuid import UUID
from fastapi import Query
from pydantic import UUID4, BaseModel, BeforeValidator, EmailStr, Field, Strict
from pydantic_core import PydanticUndefined

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
class VendorInboundCreateModel(BaseModel):

    unregistered_vendor_retailer_id: Optional[Annotated[
        UUID4, Strict(False)]] = Field(default=None)
    registered_replacement_vendor_id: Optional[Annotated[
        UUID4, Strict(False)]] = Field(default=None)
    name: str = Field(..., max_length=255)
    is_registered: Optional[bool] = Field(default=None)
    contact_email: Optional[EmailStr] = Field(default=None, max_length=320)
    contact_phone: Optional[DicsPhoneNumber] = Field(default=None,
                                                     max_length=32)
    hq_city: Optional[str] = Field(default=None, max_length=255)
    hq_state: Optional[str] = Field(default=None, max_length=255)
    hq_country: Optional[str] = Field(default=None, max_length=2, min_length=2)


# Pydantic causes these class variables to safely be instance variables.
class VendorInboundUpdateModel(BaseModel):
    name: Optional[str] = Field(default=None, max_length=255)
    unregistered_vendor_retailer_id: Optional[Annotated[
        UUID4, Strict(False)]] = Field(default=None)
    registered_replacement_vendor_id: Optional[Annotated[
        UUID4, Strict(False)]] = Field(default=None)
    is_registered: Optional[bool] = Field(default=None)
    contact_email: Optional[EmailStr] = Field(default=None, max_length=320)
    contact_phone: Optional[DicsPhoneNumber] = Field(default=None,
                                                     max_length=32)
    hq_city: Optional[str] = Field(default=None, max_length=255)
    hq_state: Optional[str] = Field(default=None, max_length=255)
    hq_country: Optional[str] = Field(default=None, max_length=2, min_length=2)


# Pydantic causes these class variables to safely be instance variables.
class VendorInboundSearchModel(CommonInboundSearchModel):
    name: Optional[str] = Query(default=None)
    name_like: Optional[str] = Query(default=None)
    is_registered: Optional[bool] = Query(default=None)
    unregistered_vendor_retailer_ids: Annotated[
        Optional[str], BeforeValidator(validate_ids)] = Query(default=None)
    registered_replacement_vendor_ids: Annotated[
        Optional[str], BeforeValidator(validate_ids)] = Query(default=None)
    hq_city: Optional[str] = Query(default=None)
    hq_state: Optional[str] = Query(default=None)
    hq_country: Optional[str] = Query(default=None)


class VendorCreateModel:

    def __init__(
        self,
        name: str,
        is_registered: bool | None = None,
        unregistered_vendor_retailer_id: UUID | None = None,
        registered_replacement_vendor_id: UUID | None = None,
        contact_email: EmailStr | None = None,
        contact_phone: DicsPhoneNumber | None = None,
        hq_city: str | None = None,
        hq_state: str | None = None,
        hq_country: str | None = None,
    ) -> None:

        self.is_registered = is_registered
        self.unregistered_vendor_retailer_id = unregistered_vendor_retailer_id
        self.registered_replacement_vendor_id = (
            registered_replacement_vendor_id)
        self.name = name
        self.contact_email = contact_email
        self.contact_phone = contact_phone
        self.hq_city = hq_city
        self.hq_state = hq_state
        self.hq_country = hq_country


class VendorUpdateModel:

    def __init__(
        self,
        name: str | None = None,
        is_registered: bool | None = None,
        unregistered_vendor_retailer_id: UUID | None = None,
        registered_replacement_vendor_id: UUID | None = None,
        contact_email: EmailStr | None = None,
        contact_phone: DicsPhoneNumber | None = None,
        hq_city: str | None = None,
        hq_state: str | None = None,
        hq_country: str | None = None,
    ) -> None:

        self.is_registered = is_registered
        self.unregistered_vendor_retailer_id = unregistered_vendor_retailer_id
        self.registered_replacement_vendor_id = (
            registered_replacement_vendor_id)
        self.name = name
        self.contact_email = contact_email
        self.contact_phone = contact_phone
        self.hq_city = hq_city
        self.hq_state = hq_state
        self.hq_country = hq_country


class VendorSearchModel(CommonSearchModel):

    def __init__(
        self,
        ids: list[UUID] | None = None,
        unregistered_vendor_retailer_ids: list[UUID] | None = None,
        registered_replacement_vendor_ids: list[UUID] | None = None,
        is_registered: bool | None = None,
        name: str | None = None,
        name_like: str | None = None,
        hq_city: str | None = None,
        hq_state: str | None = None,
        hq_country: str | None = None,
    ) -> None:

        super().__init__(ids)

        self.unregistered_vendor_retailer_ids = (
            unregistered_vendor_retailer_ids)
        self.registered_replacement_vendor_ids = (
            registered_replacement_vendor_ids)
        self.is_registered = is_registered
        self.name = name
        self.name_like = name_like
        self.hq_city = hq_city
        self.hq_state = hq_state
        self.hq_country = hq_country


class VendorDatabaseModel(CommonDatabaseModel):

    def __init__(
        self,
        id: UUID,
        name: str,
        created_at: datetime,
        is_registered: bool,
        registered_replacement_vendor_id: UUID | None = None,
        unregistered_vendor_retailer_id: UUID | None = None,
        hq_city: str | None = None,
        hq_state: str | None = None,
        hq_country: str | None = None,
        contact_email: EmailStr | None = None,
        contact_phone: DicsPhoneNumber | None = None,
        updated_at: datetime | None = None,
    ):

        super().__init__(id, created_at, updated_at)

        self.name = name
        self.registered_replacement_vendor_id = (
            registered_replacement_vendor_id)
        self.unregistered_vendor_retailer_id = unregistered_vendor_retailer_id
        self.is_registered = is_registered
        self.contact_email = contact_email
        self.contact_email = contact_phone
        self.hq_city = hq_city
        self.hq_state = hq_state
        self.hq_country = hq_country


class VendorModel(CommonModel):

    def __init__(
        self,
        id: UUID,
        name: str,
        created_at: datetime,
        is_registered: bool,
        unregistered_vendor_retailer_id: UUID | None = None,
        registered_replacement_vendor_id: UUID | None = None,
        hq_city: str | None = None,
        hq_state: str | None = None,
        hq_country: str | None = None,
        contact_email: EmailStr | None = None,
        contact_phone: DicsPhoneNumber | None = None,
        updated_at: datetime | None = None,
    ):

        super().__init__(id, created_at, updated_at)

        self.name = name
        self.registered_replacement_vendor_id = (
            registered_replacement_vendor_id)
        self.unregistered_vendor_retailer_id = unregistered_vendor_retailer_id
        self.is_registered = is_registered
        self.contact_email = contact_email
        self.contact_phone = contact_phone
        self.hq_city = hq_city
        self.hq_state = hq_state
        self.hq_country = hq_country


# Pydantic causes these class variables to safely be instance variables.
class VendorOutboundModel(CommonOutboundResponseModel):
    name: str
    is_registered: bool
    unregistered_vendor_retailer_id: UUID | None = None
    registered_replacement_vendor_id: UUID | None = None
    hq_city: str | None = None
    hq_state: str | None = None
    hq_country: str | None = None
    contact_email: EmailStr | None = None
    contact_phone: DicsPhoneNumber | None = None
