from typing import Any
from uuid import UUID
from adapters.vendor_adapters import VendorDataAdapter
from models.vendor_model import VendorCreateModel, VendorDatabaseModel, VendorModel, VendorSearchModel, VendorUpdateModel
from models.common_model import ItemList
from util.configuration import get_global_configuration
from util.database import PagingModel, SearchTerm
from util.db_connection import SelectQueryResults 
 

dblist: list[VendorDatabaseModel] = [] 

class VendorDataAccessor():  
    adapter : VendorDataAdapter =  VendorDataAdapter() 

    def insert(self, model: VendorCreateModel):
        connection = get_global_configuration().pg_connection

        db_model: dict[str, Any] = self.adapter.convert_from_create_model_to_database_model(model)

        db_result: dict[str, Any] = connection.insert("vendors", db_model)

        result_model = self.adapter.convert_from_database_model_to_model(db_result)
  
        return result_model
    
    def select_by_id(self, id: UUID):
  
        connection = get_global_configuration().pg_connection
  
        db_result = connection.select_by_id("vendors", id)

        if(db_result is None):
            return None
    
        result_model = self.adapter.convert_from_database_model_to_model(db_result)

        return result_model

    
    def select(self, model: VendorSearchModel, paging_model: PagingModel | None = None) -> ItemList[VendorModel]:
         
        connection = get_global_configuration().pg_connection
  
        search_terms: list[SearchTerm] = self.adapter.convert_from_search_model_to_search_terms(model)
        db_result: SelectQueryResults = connection.select("vendors", search_terms, paging_model)

        results: ItemList[VendorModel] = ItemList[VendorModel](db_result.paging)  
     
        if(db_result is None):
            return results

        for item in db_result.items:
            result_model = self.adapter.convert_from_database_model_to_model(item)
            results.items.append(result_model)

        return results
    
    def update(self, id: UUID, model: VendorUpdateModel, explicitNullSet: list[str] | None = None):
        
        explicitNullSet = explicitNullSet or []

        connection = get_global_configuration().pg_connection

        db_model: dict[str, Any] = self.adapter.convert_from_update_model_to_database_model(model)

        db_result  = connection.update("vendors", id, db_model)
        
        if(db_result is None):
            return None

        result_model = self.adapter.convert_from_database_model_to_model(db_result)
  
        return result_model
        
    def delete(self, id: UUID):

        connection = get_global_configuration().pg_connection
  
        db_result = connection.delete("vendors", id)

        if(db_result is None):
            return None
    
        result_model = self.adapter.convert_from_database_model_to_model(db_result)

        return result_model