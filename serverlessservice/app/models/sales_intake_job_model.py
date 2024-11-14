from datetime import datetime
from enum import Enum
from typing import Annotated, Any, Optional
from uuid import UUID
from fastapi import Query
from pydantic import UUID4, BaseModel, BeforeValidator, EmailStr, Field, Strict
from pydantic_core import PydanticUndefined
from enum import Enum


class SalesIntakeJobStatuses(str, Enum):
    Requested = 'Requested'
    Processing = 'Processing'
    Complete = 'Complete'
    Failed = 'Failed' 
 
from models.common_model import (
    CommonDatabaseModel,
    CommonInboundSearchModel,
    CommonModel,
    CommonOutboundResponseModel,
    CommonSearchModel,
    validate_ids,
)


# Pydantic causes these class variables to safely be instance variables.
class SalesIntakeJobInboundCreateModel(BaseModel):  
    retailer_location_id: Annotated[UUID4, Strict(False)] = Field(...)
    parent_batch_job_id: Annotated[Optional[UUID4], Strict(False)] = Field(default=None)
    snapshot_hour: datetime = Field(...)  
    status: Optional[SalesIntakeJobStatuses] = Field(default=None)
    status_details: Optional[dict[str,Any]] = Field(default=None)


# Pydantic causes these class variables to safely be instance variables.
class SalesIntakeJobInboundUpdateModel(BaseModel):
    status: Optional[SalesIntakeJobStatuses] = Field( default=None)
    status_details: Optional[dict[str,Any]] = Field(default=None)



# Pydantic causes these class variables to safely be instance variables.
class SalesIntakeJobInboundSearchModel(CommonInboundSearchModel): 
    snapshot_hour_min: Optional[datetime] = Query(default=None)
    snapshot_hour_max: Optional[datetime] = Query(default=None)
    status: Optional[SalesIntakeJobStatuses] = Query(default=None)
    retailer_ids: Annotated[Optional[str], BeforeValidator(validate_ids)] = Query(default=None) 
    retailer_location_ids: Annotated[Optional[str], BeforeValidator(validate_ids)] = Query(default=None) 
    parent_batch_job_ids: Annotated[Optional[str], BeforeValidator(validate_ids)] = Query(default=None) 


class SalesIntakeJobCreateModel:

    def __init__(
        self,
        retailer_location_id: UUID , 
        snapshot_hour: datetime,
        retailer_id: UUID | None = None,
        parent_batch_job_id: UUID | None = None,
        status: SalesIntakeJobStatuses | None = None,
        status_details: dict[str,Any] | None = None,
        
    ) -> None:
 
        self.retailer_location_id = retailer_location_id
        self.parent_batch_job_id = parent_batch_job_id
        self.retailer_id = retailer_id
        self.snapshot_hour = snapshot_hour
        self.status = status
        self.status_details = status_details


class SalesIntakeJobUpdateModel:

    def __init__(
        self,
        status: SalesIntakeJobStatuses | None = None,
        status_details: dict[str,Any] | None = None,
            
        
    ) -> None:

        self.status = status
        self.status_details = status_details
 
class SalesIntakeJobSearchModel(CommonSearchModel):

    def __init__(
        self,
        ids: list[UUID] | None = None,
        retailer_ids: list[UUID] | None = None,
        retailer_location_ids: list[UUID] | None = None,
        parent_batch_job_ids: list[UUID] | None = None,
        snapshot_hour_min: datetime | None = None,
        snapshot_hour_max: datetime | None = None,
        status: SalesIntakeJobStatuses | None = None,
    ) -> None:

        super().__init__(ids)

        self.retailer_ids = retailer_ids
        self.retailer_location_ids = retailer_location_ids
        self.parent_batch_job_ids = parent_batch_job_ids
        self.snapshot_hour_min = snapshot_hour_min
        self.snapshot_hour_max = snapshot_hour_max
        self.status = status


class SalesIntakeJobModel(CommonModel):

    def __init__(
        self,
        id: UUID,
        retailer_id: UUID,
        retailer_location_id: UUID,
        snapshot_hour: datetime,
        status: SalesIntakeJobStatuses,
        status_details: dict[str,Any], 
        created_at: datetime, 
        parent_batch_job_id: UUID | None = None,
        updated_at: datetime | None = None,
    ):

        super().__init__(id, created_at, updated_at)

        self.retailer_id = retailer_id
        self.retailer_location_id = retailer_location_id        
        self.parent_batch_job_id = parent_batch_job_id        
        self.snapshot_hour = snapshot_hour
        self.status = status
        self.status_details = status_details


class SalesIntakeJobDatabaseModel(CommonDatabaseModel):

    def __init__(
        self,
        id: UUID,
        retailer_id: UUID,
        retailer_location_id: UUID,
        snapshot_hour: datetime,
        status: SalesIntakeJobStatuses,
        status_details: dict[str,Any],
        created_at: datetime, 
        parent_batch_job_id: UUID | None = None,
        updated_at: datetime | None = None,
    ):

        super().__init__(id, created_at, updated_at)

        self.retailer_id = retailer_id
        self.retailer_location_id = retailer_location_id
        self.parent_batch_job_id = parent_batch_job_id
        self.snapshot_hour = snapshot_hour
        self.status = status
        self.status_details = status_details


# Pydantic causes these class variables to safely be instance variables.
class SalesIntakeJobOutboundModel(CommonOutboundResponseModel):
    retailer_id: UUID   
    retailer_location_id: UUID
    parent_batch_job_id: UUID | None = None
    snapshot_hour: str
    status: SalesIntakeJobStatuses 
    status_details: dict[str,Any] 
