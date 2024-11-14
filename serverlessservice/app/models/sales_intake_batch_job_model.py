from datetime import datetime
from enum import Enum
from typing import Annotated, Any, Optional
from uuid import UUID
from fastapi import Query
from pydantic import UUID4, BaseModel, BeforeValidator, EmailStr, Field, Strict
from pydantic_core import PydanticUndefined
from enum import Enum


class SalesIntakeBatchJobStatuses(str, Enum):
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
class SalesIntakeBatchJobInboundCreateModel(BaseModel):   
    start_time: datetime = Field(...)  
    end_time: Optional[datetime] = Field(default=None)  
    restricted_retailer_location_ids: Annotated[Optional[str | list[str]], BeforeValidator(validate_ids)] = Field(default=None)
    status: Optional[SalesIntakeBatchJobStatuses] = Field(default=None) 
    status_details: Optional[dict[str,Any]] = Field(default=None)


# Pydantic causes these class variables to safely be instance variables.
class SalesIntakeBatchJobInboundUpdateModel(BaseModel):
    status: Optional[SalesIntakeBatchJobStatuses] = Field( default=None)
    status_details: Optional[dict[str,Any]] = Field(default=None)

# Pydantic causes these class variables to safely be instance variables.
class SalesIntakeBatchJobInboundSearchModel(CommonInboundSearchModel): 
    start_time_min: Optional[datetime] = Query(default=None)
    start_time_max: Optional[datetime] = Query(default=None)
    end_time_min: Optional[datetime] = Query(default=None)
    end_time_max: Optional[datetime] = Query(default=None) 
    status: Optional[SalesIntakeBatchJobStatuses] = Query(default=None) 


class SalesIntakeBatchJobCreateModel:

    def __init__(
        self, 
        start_time: datetime,
        end_time: datetime | None = None, 
        status: SalesIntakeBatchJobStatuses | None = None,
        status_details: dict[str,Any] | None = None,
        restricted_retailer_location_ids: list[UUID] | None = None,
        
    ) -> None:
        
        self.start_time = start_time
        self.end_time = end_time
        self.status = status
        self.status_details = status_details
        self.restricted_retailer_location_ids = restricted_retailer_location_ids


class SalesIntakeBatchJobUpdateModel:

    def __init__(
        self,
        status: SalesIntakeBatchJobStatuses | None = None,
        status_details: dict[str,Any] | None = None,
            
        
    ) -> None:

        self.status = status
        self.status_details = status_details
 
class SalesIntakeBatchJobSearchModel(CommonSearchModel):

    def __init__(
        self,
        ids: list[UUID] | None = None,  
        start_time_min: datetime | None = None,
        start_time_max: datetime | None = None,
        end_time_min: datetime | None = None,
        end_time_max: datetime | None = None,
        status: SalesIntakeBatchJobStatuses | None = None,
    ) -> None:

        super().__init__(ids)

        self.start_time_min = start_time_min
        self.start_time_max = start_time_max
        self.end_time_min = end_time_min
        self.end_time_max = end_time_max
        self.status = status


class SalesIntakeBatchJobModel(CommonModel):

    def __init__(
        self,
        id: UUID, 
        start_time: datetime,
        status: SalesIntakeBatchJobStatuses,
        status_details: dict[str,Any],
        created_at: datetime, 
        restricted_retailer_location_ids: list[UUID] | None = None,
        end_time: datetime | None = None,
        updated_at: datetime | None = None,
    ):

        super().__init__(id, created_at, updated_at)

        self.start_time = start_time    
            
        self.status = status
        self.status_details = status_details
        self.restricted_retailer_location_ids = restricted_retailer_location_ids
        self.end_time = end_time


class SalesIntakeBatchJobDatabaseModel(CommonDatabaseModel):

    def __init__(
        self,
        id: UUID, 
        start_time: datetime,
        status: SalesIntakeBatchJobStatuses,
        status_details: dict[str,Any],
        created_at: datetime,
        end_time: datetime  | None = None,
        restricted_retailer_location_ids: list[UUID] | None = None,
        updated_at: datetime | None = None,
    ):

        super().__init__(id, created_at, updated_at)

  
        self.status = status
        self.status_details = status_details
        self.start_time = start_time
        self.end_time = end_time
        self.restricted_retailer_location_ids = restricted_retailer_location_ids


# Pydantic causes these class variables to safely be instance variables.
class SalesIntakeBatchJobOutboundModel(CommonOutboundResponseModel):
    
    start_time: str
    end_time: str | None = None
    status: SalesIntakeBatchJobStatuses
    
    restricted_retailer_location_ids: list[UUID] | None = None,
    status_details: dict[str,Any]
