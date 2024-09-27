from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID
from fastapi import Query
from pydantic import BaseModel, EmailStr, Field
from pydantic_core import PydanticUndefined
from enum import Enum

class PosPlatforms(str, Enum):
    Posabit = 'Posabit'
    Flowhub = 'Flowhub'
    Dutchie = 'Dutchie'
    KlickTrack = 'KlickTrack'
    Cova = 'Cova'
    Meadow = 'Meadow'
    GrowFlow = 'GrowFlow'
    Unknown = 'Unknown'
    
from models.common_model import CommonDatabaseModel, CommonInboundSearchModel, CommonModel, CommonOutboundResponseModel, CommonSearchModel

# Pydantic causes these class variables to safely be instance variables.
class PosIntegrationInboundCreateModel(BaseModel):   
    name: str = Field(..., max_length=255)
    description: Optional[str] = Field(default=None) 
    pos_platform: Optional[PosPlatforms] = Field(...)  

# Pydantic causes these class variables to safely be instance variables.
class PosIntegrationInboundUpdateModel(BaseModel): 
    name: Optional[str] = Field(default=None, max_length=255)
    description: Optional[str] = Field(default=None) 
    pos_platform: Optional[PosPlatforms] = Field(default=None)  

# Pydantic causes these class variables to safely be instance variables.
class PosIntegrationInboundSearchModel(CommonInboundSearchModel):
    name: Optional[str] = Query(default=None)
    name_like: Optional[str] = Query(default=None) 
    pos_platform: Optional[PosPlatforms] = Query(default = None) 

class PosIntegrationCreateModel():  

    def __init__(self,
                name: str, 
                pos_platform: PosPlatforms,
                description: str | None = None) -> None:
        
        self.name = name 
        self.pos_platform = pos_platform 
        self.description = description 

class PosIntegrationUpdateModel():  

    def __init__(self,
                name: str | None = None,
                pos_platform: str | None = None,
                description: str | None = None) -> None:
            
        self.name = name 
        self.pos_platform = pos_platform 
        self.description = description 

class PosIntegrationSearchModel(CommonSearchModel):  
    
    def __init__(self,
                ids: list[UUID] | None = None,
                name: str | None = None,
                name_like: str | None = None,
                pos_platform: PosPlatforms | None = None) -> None:
                
        super().__init__(ids)

        self.name = name
        self.name_like = name_like 
        self.pos_platform = pos_platform

class PosIntegrationModel(CommonModel): 

    def __init__(self, 
                id: UUID,
                name: str,
                pos_platform: PosPlatforms,
                created_at: datetime, 
                description: str | None = None, 
                updated_at: datetime | None = None):
         
        super().__init__(id, created_at, updated_at)
        
        self.name = name
        self.pos_platform = pos_platform
        self.description = description 
         
class PosIntegrationDatabaseModel(CommonDatabaseModel):  
    def __init__(self,
                id: UUID,
                name: str,
                pos_platform: PosPlatforms,
                created_at: datetime, 
                description: str | None = None, 
                updated_at: datetime | None = None):
        
        super().__init__(id, created_at, updated_at)
 
        self.name = name
        self.pos_platform = pos_platform
        self.description = description 

# Pydantic causes these class variables to safely be instance variables.
class PosIntegrationOutboundModel(CommonOutboundResponseModel):   
    name: str
    pos_platform: PosPlatforms | None = None
    description: str | None = None 

